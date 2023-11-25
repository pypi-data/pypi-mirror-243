import jax
import jax.numpy as jnp
from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'adabelief'
]


AdaBeliefState = namedtuple(
  'AdaBeliefState',
  ['first_momentum', 'second_momentum', 'effective_beta1', 'effective_beta2']
)

class adabelief(GradientOptimizer):
  State = AdaBeliefState

  def __init__(self, learning_rate=1e-3, beta1=0.9, beta2=0.999, eps=1e-8):
    super(adabelief, self).__init__()

    self.learning_rate = learning_rate
    self.beta1 = beta1
    self.beta2 = beta2

    self.eps = eps

  def initial_state(self, parameters: Parameters) -> AdaBeliefState:
    from .. import utils
    dtype = utils.dtype.get_common_dtype(parameters)

    return AdaBeliefState(
      first_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      effective_beta1=jnp.ones(shape=tuple(), dtype=dtype),
      effective_beta2=jnp.ones(shape=tuple(), dtype=dtype),
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: AdaBeliefState
  ) -> tuple[Parameters, AdaBeliefState]:
    first_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: self.beta1 * m + (1 - self.beta1) * g,
      state.first_momentum, gradient
    )

    second_momentum_updated = jax.tree_util.tree_map(
      lambda s, m, g: self.beta2 * s + (1 - self.beta2) * jnp.square(g - m) + self.eps,
      state.second_momentum, state.first_momentum, gradient
    )

    effective_beta1 = state.effective_beta1 * self.beta1
    effective_beta2 = state.effective_beta2 * self.beta2

    effective_learning_rate = self.learning_rate * jnp.sqrt(1 - effective_beta2) / (1 - effective_beta1)

    updated_parameters = jax.tree_util.tree_map(
      lambda x, m, s: x - effective_learning_rate * m / (jnp.sqrt(s) + self.eps),
      parameters, first_momentum_updated, second_momentum_updated
    )

    return updated_parameters, AdaBeliefState(
      first_momentum=first_momentum_updated,
      second_momentum=second_momentum_updated,
      effective_beta1=effective_beta1,
      effective_beta2=effective_beta2
    )