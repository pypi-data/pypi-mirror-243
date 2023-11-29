from pathlib import Path
from functools import partial
from collections import namedtuple

import torch
import torch.nn.functional as F
import torch.distributed as dist
from torch import nn, einsum, Tensor
from torch.nn import Module, ModuleList
from torch.utils.data import Dataset, DataLoader

from torchtyping import TensorType

from einops import rearrange, repeat, pack, unpack
from einops.layers.torch import Rearrange

from beartype import beartype
from beartype.typing import Optional, Union, List, Tuple

from q_transformer.robotic_transformer import QRoboticTransformer

from q_transformer.optimizer import get_adam_optimizer

from accelerate import Accelerator

from ema_pytorch import EMA

# constants

QIntermediates = namedtuple('QIntermediates', [
    'q_pred_all_actions',
    'q_pred',
    'q_next',
    'q_target'
])

Losses = namedtuple('Losses', [
    'td_loss',
    'conservative_reg_loss'
])

# helpers

def exists(val):
    return val is not None

def is_divisible(num, den):
    return (num % den) == 0

def repeat_tuple_el(t: Tuple, i: int) -> Tuple:
    out = []
    for el in t:
        for _ in range(i):
            out.append(el)
    return tuple(out)

def pack_one(t, pattern):
    return pack([t], pattern)

def unpack_one(t, ps, pattern):
    return unpack(t, ps, pattern)[0]

def cycle(dl):
    while True:
        for batch in dl:
            yield batch

# tensor helpers

def batch_select_indices(t, indices):
    batch = t.shape[0]
    batch_arange = torch.arange(batch, device = indices.device)
    batch_arange = rearrange(batch_arange, 'b -> b 1')
    indices = rearrange(indices, 'b -> b 1')
    selected = t[batch_arange, indices]
    return rearrange(selected, 'b 1 -> b')

# Q learning on robotic transformer

class QLearner(Module):

    @beartype
    def __init__(
        self,
        model: Union[QRoboticTransformer, Module],
        *,
        dataset: Dataset,
        batch_size: int,
        num_train_steps: int,
        learning_rate: float,
        weight_decay: float = 0.,
        accelerator: Optional[Accelerator] = None,
        accelerator_kwargs: dict = dict(),
        dataloader_kwargs: dict = dict(
            shuffle = True
        ),
        q_target_ema_kwargs: dict = dict(
            beta = 0.99,
            update_after_step = 10,
            update_every = 5
        ),
        n_step_q_learning = False,
        discount_factor_gamma = 0.98,
        conservative_reg_loss_weight = 1., # they claim 1. is best in paper
        optimizer_kwargs: dict = dict(),
        checkpoint_folder = './checkpoints',
        checkpoint_every = 1000,
    ):
        super().__init__()
        assert model.num_actions == 1

        # q-learning related hyperparameters

        self.discount_factor_gamma = discount_factor_gamma
        self.n_step_q_learning = n_step_q_learning
        self.conservative_reg_loss_weight = conservative_reg_loss_weight

        self.register_buffer('discount_matrix', None, persistent = False)

        # online (evaluated) Q model

        self.model = model

        # ema (target) Q model

        self.ema_model = EMA(
            model,
            include_online_model = False,
            **q_target_ema_kwargs
        )

        self.optimizer = get_adam_optimizer(
            model.parameters(),
            lr = learning_rate,
            wd = weight_decay,
            **optimizer_kwargs
        )

        if not exists(accelerator):
            accelerator = Accelerator(**accelerator_kwargs)

        self.accelerator = accelerator

        self.dataloader = DataLoader(
            dataset,
            batch_size = batch_size,
            **dataloader_kwargs
        )

        # prepare

        (
            self.model,
            self.ema_model,
            self.optimizer,
            self.dataloader
        ) = self.accelerator.prepare(
            self.model,
            self.ema_model,
            self.optimizer,
            self.dataloader
        )

        # checkpointing related

        self.checkpoint_every = checkpoint_every
        self.checkpoint_folder = Path(checkpoint_folder)

        self.checkpoint_folder.mkdir(exist_ok = True, parents = True)
        assert self.checkpoint_folder.is_dir()

        # training step related

        self.num_train_steps = num_train_steps
        self.register_buffer('step', torch.tensor(0))

    def save(
        self,
        checkpoint_num = None,
        overwrite = True
    ):
        name = 'checkpoint'
        if exists(checkpoint_num):
            name += f'-{checkpoint_num}'

        path = self.checkpoint_folder / (name + '.pt')

        assert overwrite or not path.exists()

        pkg = dict(
            model = self.unwrap(self.model).state_dict(),
            ema_model = self.unwrap(self.ema_model).state_dict(),
            optimizer = self.optimizer.state_dict()
        )

        torch.save(pkg, str(path))

    def load(self, path):
        path = Path(path)
        assert exists(path)

        pkg = torch.load(str(path))

        self.unwrap(self.model).load_state_dict(pkg['model'])
        self.unwrap(self.ema_model).load_state_dict(pkg['ema_model'])

        self.optimizer.load_state_dict(pkg['optimizer'])

    @property
    def device(self):
        return self.accelerator.device

    @property
    def is_main(self):
        return self.accelerator.is_main_process

    def unwrap(self, module):
        return self.accelerator.unwrap_model(module)

    def print(self, msg):
        return self.accelerator.print(msg)

    def wait(self):
        return self.accelerator.wait_for_everyone()

    def get_discount_matrix(self, timestep):
        if exists(self.discount_matrix) and self.discount_matrix.shape[-1] >= timestep:
            return self.discount_matrix[:timestep, :timestep]

        timestep_arange = torch.arange(timestep, device = self.accelerator.device)
        powers = (timestep_arange[None, :] - timestep_arange[:, None])
        discount_matrix = torch.triu(self.discount_factor_gamma ** powers)

        self.register_buffer('discount_matrix', discount_matrix, persistent = False)
        return self.discount_matrix

    def q_learn(
        self,
        instructions:   Tuple[str],
        states:         TensorType['b', 'c', 'f', 'h', 'w', float],
        actions:        TensorType['b', int],
        next_states:    TensorType['b', 'c', 'f', 'h', 'w', float],
        reward:         TensorType['b', float],
        done:           TensorType['b', bool]
    ) -> Tuple[Tensor, QIntermediates]:
        # 'next' stands for the very next time step (whether state, q, actions etc)

        γ = self.discount_factor_gamma
        not_terminal = (~done).float()

        # first make a prediction with online q robotic transformer
        # select out the q-values for the action that was taken

        q_pred_all_actions = self.model(states, instructions)
        q_pred = batch_select_indices(q_pred_all_actions, actions)

        # use an exponentially smoothed copy of model for the future q target. more stable than setting q_target to q_eval after each batch
        # the max Q value is taken as the optimal action is implicitly the one with the highest Q score

        q_next = self.ema_model(next_states, instructions).amax(dim = -1)

        # Bellman's equation. most important line of code, hopefully done correctly

        q_target = reward + not_terminal * (γ * q_next)

        # now just force the online model to be able to predict this target

        loss = F.mse_loss(q_pred, q_target)

        # that's it. 4 loc for the heart of q-learning
        # return loss and some of the intermediates for logging

        return loss, QIntermediates(q_pred, q_next, q_target)

    def n_step_q_learn(
        self,
        instructions:   Tuple[str],
        states:         TensorType['b', 't', 'c', 'f', 'h', 'w', float],
        actions:        TensorType['b', 't', int],
        next_states:    TensorType['b', 'c', 'f', 'h', 'w', float],
        rewards:        TensorType['b', 't', float],
        dones:          TensorType['b', 't', bool]
    ) -> Tuple[Tensor, QIntermediates]:
        """
        einops

        b - batch
        c - channels
        f - frames
        h - height
        w - width
        t - timesteps
        a - action bins
        q - q values
        """

        num_timesteps, device = states.shape[1], states.device

        # fold time steps into batch

        states, time_ps = pack_one(states, '* c f h w')

        # repeat instructions per timestep

        repeated_instructions = repeat_tuple_el(instructions, num_timesteps)

        γ = self.discount_factor_gamma

        # anything after the first done flag will be considered terminal

        dones = dones.cumsum(dim = -1) > 0
        dones = F.pad(dones, (1, 0), value = False)

        not_terminal = (~dones).float()

        # get q predictions

        actions = rearrange(actions, 'b t -> (b t)')

        q_pred_all_actions = self.model(states, repeated_instructions)
        q_pred = batch_select_indices(q_pred_all_actions, actions)
        q_pred = unpack_one(q_pred, time_ps, '*')

        q_next = self.ema_model(next_states, instructions).amax(dim = -1)

        # prepare rewards and discount factors across timesteps

        rewards, _ = pack([rewards, q_next], 'b *')

        γ = self.get_discount_matrix(num_timesteps + 1)[:-1, :]

        # account for discounting using the discount matrix

        q_target = einsum('b t, q t -> b q', not_terminal * rewards, γ)

        # have transformer learn to predict above Q target

        loss = F.mse_loss(q_pred, q_target)

        # prepare q prediction

        q_pred_all_actions = unpack_one(q_pred_all_actions, time_ps, '* a')

        return loss, QIntermediates(q_pred_all_actions, q_pred, q_next, q_target)

    def learn(
        self,
        *args
    ):
        _, _, actions, *_ = args

        # main q-learning loss, whether single or n-step

        if self.n_step_q_learning:
            td_loss, q_intermediates = self.n_step_q_learn(*args)
        else:
            td_loss, q_intermediates = self.q_learn(*args)

        # calculate conservative regularization

        batch = actions.shape[0]

        q_preds = q_intermediates.q_pred_all_actions
        num_action_bins = q_preds.shape[-1]
        num_non_dataset_actions = num_action_bins - 1

        actions = rearrange(actions, '... -> ... 1')

        dataset_action_mask = torch.zeros_like(q_preds).scatter_(-1, actions, torch.ones_like(q_preds))

        q_actions_not_taken = q_preds[~dataset_action_mask.bool()]
        q_actions_not_taken = rearrange(q_actions_not_taken, '(b t a) -> b t a', b = batch, a = num_non_dataset_actions)

        conservative_reg_loss = (q_actions_not_taken ** 2).sum() / num_non_dataset_actions

        # total loss

        loss =  0.5 * td_loss + \
                0.5 * conservative_reg_loss * self.conservative_reg_loss_weight

        loss_breakdown = Losses(td_loss, conservative_reg_loss)

        return loss, loss_breakdown

    def forward(self):
        step = self.step.item()

        replay_buffer_iter = cycle(self.dataloader)

        self.model.train()
        self.ema_model.train()

        while step < self.num_train_steps:

            # zero grads

            self.optimizer.zero_grad()

            # main q-learning algorithm

            with self.accelerator.autocast():

                loss, (td_loss, conservative_reg_loss) = self.learn(*next(replay_buffer_iter))

                self.accelerator.backward(loss)

            self.print(f'td loss: {td_loss.item():.3f}')

            # take optimizer step

            self.optimizer.step()

            # update target ema

            self.wait()

            self.ema_model.update()

            # increment step

            step += 1
            self.step.add_(1)

            # whether to checkpoint or not

            self.wait()

            if self.is_main and is_divisible(step, self.checkpoint_every):
                checkpoint_num = step // self.checkpoint_every
                self.save(checkpoint_num)

            self.wait()

        self.print('training complete')
