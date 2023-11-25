import jax
from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'sgd',
  'momentum'
]

SGDState = None

class sgd(GradientOptimizer):
  State = SGDState

  def __init__(self, learning_rate=1e-3):
    super(sgd, self).__init__()
    self.learning_rate = learning_rate

  def initial_state(self, parameters: Parameters) -> SGDState:
    return None

  def __call__(self, parameters: Parameters, gradient: Parameters, state: SGDState) -> tuple[Parameters, SGDState]:

    updated_parameters = jax.tree_util.tree_map(
      lambda x, g: x - self.learning_rate * g,
      parameters, gradient
    )

    return updated_parameters, None


MomentumState = namedtuple(
  'MomentumState',
  ['momentum']
)

class momentum(GradientOptimizer):
  State = MomentumState

  def __init__(self, learning_rate=1e-3, rho=0.9):
    super(momentum, self).__init__()
    self.learning_rate = learning_rate
    self.rho = rho

  def initial_state(self, parameters: Parameters) -> MomentumState:
    return MomentumState(
      momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters)
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: MomentumState
) -> tuple[Parameters, MomentumState]:

    updated_momentum = jax.tree_util.tree_map(
      lambda m, g: self.rho * m + (1 - self.rho) * g,
      state.momentum, gradient
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, m: x - self.learning_rate * m,
      parameters, updated_momentum
    )

    return updated_parameters, MomentumState(momentum=updated_momentum)