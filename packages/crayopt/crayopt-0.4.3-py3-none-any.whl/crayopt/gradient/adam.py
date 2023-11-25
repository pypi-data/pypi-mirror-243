import jax
import jax.numpy as jnp
from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'adam', 'adamax', 'ladamax'
]


AdamState = namedtuple(
  'AdamState',
  ['first_momentum', 'second_momentum', 'effective_beta1', 'effective_beta2']
)

class adam(GradientOptimizer):
  State = AdamState

  def __init__(self, learning_rate=1e-3, beta1=0.9, beta2=0.999, eps=1e-8):
    super(adam, self).__init__()
    self.learning_rate = learning_rate
    self.beta1 = beta1
    self.beta2 = beta2

    self.eps = eps

  def initial_state(self, parameters: Parameters) -> AdamState:
    from .. import utils
    dtype = utils.dtype.get_common_dtype(parameters)

    return AdamState(
      first_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      effective_beta1=jnp.ones(shape=tuple(), dtype=dtype),
      effective_beta2=jnp.ones(shape=tuple(), dtype=dtype),
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: AdamState
  ) -> tuple[Parameters, AdamState]:
    first_momentum_updated = jax.tree_util.tree_map(
      lambda v, g: self.beta1 * v + (1 - self.beta1) * g,
      state.first_momentum, gradient
    )

    second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: self.beta2 * m + (1 - self.beta2) * jnp.square(g),
      state.second_momentum, gradient
    )

    effective_beta1 = state.effective_beta1 * self.beta1
    effective_beta2 = state.effective_beta2 * self.beta2

    effective_learning_rate = self.learning_rate * jnp.sqrt(1 - effective_beta2) / (1 - effective_beta1)

    updated_parameters = jax.tree_util.tree_map(
      lambda x, v, m: x - effective_learning_rate * v / (jnp.sqrt(m) + self.eps),
      parameters, first_momentum_updated, second_momentum_updated
    )

    return updated_parameters, AdamState(
      first_momentum=first_momentum_updated,
      second_momentum=second_momentum_updated,
      effective_beta1=effective_beta1,
      effective_beta2=effective_beta2
    )


AdamaxState = namedtuple(
  'AdamaxState',
  ['first_momentum', 'second_momentum', 'effective_beta1']
)

class adamax(GradientOptimizer):
  State = AdamaxState

  def __init__(self, learning_rate=2e-3, beta1=0.9, beta2=0.999, eps=1e-8):
    super(adamax, self).__init__()
    self.learning_rate = learning_rate
    self.beta1 = beta1
    self.beta2 = beta2

    self.eps = eps

  def initial_state(self, parameters: Parameters) -> AdamaxState:
    from .. import utils
    dtype = utils.dtype.get_common_dtype(parameters)

    return AdamaxState(
      first_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      effective_beta1=jnp.ones(shape=tuple(), dtype=dtype),
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: AdamaxState
  ) -> tuple[Parameters, AdamaxState]:
    first_momentum_updated = jax.tree_util.tree_map(
      lambda v, g: self.beta1 * v + (1 - self.beta1) * g,
      state.first_momentum, gradient
    )

    second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: jnp.maximum(self.beta2 * m, jnp.abs(g)),
      state.second_momentum, gradient
    )

    effective_beta1 = state.effective_beta1 * self.beta1

    effective_learning_rate = self.learning_rate / (1 - effective_beta1)

    updated_parameters = jax.tree_util.tree_map(
      lambda x, v, m: x - effective_learning_rate * v / (m + self.eps),
      parameters, first_momentum_updated, second_momentum_updated
    )

    return updated_parameters, AdamaxState(
      first_momentum=first_momentum_updated,
      second_momentum=second_momentum_updated,
      effective_beta1=effective_beta1,
    )


LAdamaxState = namedtuple(
  'LAdamaxState',
  ['second_momentum']
)

class ladamax(GradientOptimizer):
  """
  Light AdaMax without first momentum for non-stochastic optimization.
  """
  State = LAdamaxState

  def __init__(self, learning_rate=2e-3, beta2=0.999, eps=1e-8):
    super(ladamax, self).__init__()
    self.learning_rate = learning_rate
    self.beta2 = beta2

    self.eps = eps

  def initial_state(self, parameters: Parameters) -> LAdamaxState:
    return LAdamaxState(
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: LAdamaxState
  ) -> tuple[Parameters, LAdamaxState]:
    second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: jnp.maximum(self.beta2 * m, jnp.abs(g)),
      state.second_momentum, gradient
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, g, m: x - self.learning_rate * g / (m + self.eps),
      parameters, gradient, second_momentum_updated
    )

    return updated_parameters, LAdamaxState(second_momentum=second_momentum_updated)