import jax
import jax.numpy as jnp
from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'rmsprop', 'rmsmax'
]


RMSPropState = namedtuple(
  'RMSPropState',
  ['second_momentum']
)

class rmsprop(GradientOptimizer):
  State = RMSPropState

  def __init__(self, learning_rate=1e-3, rho=0.9, eps=1e-6):
    super(rmsprop, self).__init__()
    self.learning_rate = learning_rate
    self.rho = rho
    self.eps = eps

  def initial_state(self, parameters: Parameters) -> RMSPropState:
    return RMSPropState(
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters)
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: RMSPropState
) -> tuple[Parameters, RMSPropState]:

    updated_second_momentum = jax.tree_util.tree_map(
      lambda m, g: self.rho * m + (1 - self.rho) * jnp.square(g),
      state.second_momentum, gradient
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, g, m: x - self.learning_rate * g / jnp.sqrt(m + self.eps),
      parameters, gradient, updated_second_momentum
    )

    return updated_parameters, RMSPropState(second_momentum=updated_second_momentum)


RMSMaxState = namedtuple(
  'RMSMaxState',
  ['second_momentum']
)

class rmsmax(GradientOptimizer):
  State = RMSMaxState

  def __init__(self, learning_rate=1e-3, rho=0.9, eps=1e-6):
    super(rmsmax, self).__init__()
    self.learning_rate = learning_rate
    self.rho = rho
    self.eps = eps

  def initial_state(self, parameters: Parameters) -> RMSMaxState:
    return RMSMaxState(
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters)
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: RMSMaxState
  ) -> tuple[Parameters, RMSMaxState]:

    updated_second_momentum = jax.tree_util.tree_map(
      lambda m, g: jnp.maximum(self.rho * m, jnp.abs(g)),
      state.second_momentum, gradient
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, g, m: x - self.learning_rate * g / (m + self.eps),
      parameters, gradient, updated_second_momentum
    )

    return updated_parameters, RMSMaxState(second_momentum=updated_second_momentum)