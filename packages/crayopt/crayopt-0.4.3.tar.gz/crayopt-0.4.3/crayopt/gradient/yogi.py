import jax
import jax.numpy as jnp
from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'yogi'
]


YogiState = namedtuple(
  'YogiState',
  ['first_momentum', 'second_momentum']
)

class yogi(GradientOptimizer):
  State = YogiState

  def __init__(self, learning_rate=1e-3, beta1=0.9, beta2=0.999, eps=1e-3):
    super(yogi, self).__init__()

    self.learning_rate = learning_rate
    self.beta1 = beta1
    self.beta2 = beta2

    self.eps = eps

  def initial_state(self, parameters: Parameters) -> YogiState:
    from .. import utils
    dtype = utils.dtype.get_common_dtype(parameters)

    return YogiState(
      first_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: YogiState
  ) -> tuple[Parameters, YogiState]:
    first_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: self.beta1 * m + (1 - self.beta1) * g,
      state.first_momentum, gradient
    )

    second_momentum_updated = jax.tree_util.tree_map(
      lambda v, m, g: v - (1 - self.beta2) * jnp.sign(m - jnp.square(g)) * jnp.square(g),
      state.second_momentum, state.first_momentum, gradient
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, m, v: x - self.learning_rate * m / (jnp.sqrt(v) + self.eps),
      parameters, first_momentum_updated, second_momentum_updated
    )

    return updated_parameters, YogiState(
      first_momentum=first_momentum_updated,
      second_momentum=second_momentum_updated,
    )