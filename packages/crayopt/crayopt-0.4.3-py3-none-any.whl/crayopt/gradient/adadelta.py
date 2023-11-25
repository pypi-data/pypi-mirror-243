import jax
import jax.numpy as jnp

from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'adadelta'
]

AdadeltaState = namedtuple(
  'AdadeltaState',
  ['delta_average', 'second_momentum']
)

class adadelta(GradientOptimizer):
  State = AdadeltaState

  def __init__(self, learning_rate=1e-1, rho=0.9, eps=1e-6):
    super(adadelta, self).__init__()
    self.learning_rate = learning_rate
    self.rho = rho
    self.eps = eps

  def initial_state(self, parameters: Parameters) -> AdadeltaState:
    return AdadeltaState(
      delta_average=jax.tree_util.tree_map(
        lambda x: jnp.zeros_like(x),
        parameters
      ),
      second_momentum=jax.tree_util.tree_map(
        lambda x: jnp.zeros_like(x),
        parameters
      )
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: AdadeltaState
  ) -> tuple[Parameters, AdadeltaState]:

    updated_second_momentum = jax.tree_util.tree_map(
      lambda m, g: self.rho * m + (1 - self.rho) * jnp.square(g),
      state.second_momentum, gradient
    )

    deltas = jax.tree_util.tree_map(
      lambda d, m, g: jnp.sqrt(d + self.eps) / jnp.sqrt(m + self.eps) * g,
      state.delta_average, updated_second_momentum, gradient
    )

    updated_deltas = jax.tree_util.tree_map(
      lambda dm, d: self.rho * dm + (1 - self.rho) * jnp.square(d),
      state.delta_average, deltas
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, d: x - self.learning_rate * d,
      parameters, deltas
    )

    return updated_parameters, AdadeltaState(
      second_momentum=updated_second_momentum,
      delta_average=updated_deltas
    )