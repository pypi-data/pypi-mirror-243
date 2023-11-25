import jax
import jax.numpy as jnp
from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'adagrad'
]


AdaGradState = namedtuple(
  'AdaGradState',
  ['second_momentum']
)

class adagrad(GradientOptimizer):
  State = AdaGradState

  def __init__(self, learning_rate=1e-2, eps=1e-6):
    super(adagrad, self).__init__()
    self.learning_rate = learning_rate
    self.eps = eps

  def initial_state(self, parameters: Parameters) -> AdaGradState:
    return AdaGradState(
      second_momentum=jax.tree_util.tree_map(
        lambda x: jax.numpy.zeros_like(x),
        parameters
      )
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: AdaGradState
  ) -> tuple[Parameters, AdaGradState]:

    updated_second_momentum = jax.tree_util.tree_map(
      lambda m, g: m + jnp.square(g),
      state.second_momentum, gradient
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, g, m: x - self.learning_rate * g / jnp.sqrt(m + self.eps),
      parameters, gradient, updated_second_momentum
    )

    return updated_parameters, AdaGradState(second_momentum=updated_second_momentum)