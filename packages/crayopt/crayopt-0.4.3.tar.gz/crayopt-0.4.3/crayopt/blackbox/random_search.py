from typing import Union, Optional
from collections import namedtuple

from .meta import BlackBoxOptimizer, Parameters

import jax
import jax.numpy as jnp

__all__ = [
  'LRS', 'GRS', 'RandomSearchState',
  'MRS', 'LinMRS', 'MRSState', 'DMRS', 'DMRSState',
  'RSS', 'RSSState'
]

RandomSearchState = namedtuple('RandomSearchState', ['parameters', 'value'])

class RandomSearch(BlackBoxOptimizer):
  OptimizerState = RandomSearchState

  def initial_state(self, parameters: Parameters) -> RandomSearchState:
    return RandomSearchState(
      parameters=parameters,
      ### as the value is unknown
      value=jnp.inf,
    )

  def propose(self, rng: jax.Array, state: RandomSearchState, batch: tuple[int, ...]=()) -> Parameters:
    raise NotImplementedError()

  def __call__(
    self, parameters: Parameters, value: Union[float, jax.numpy.ndarray], state: RandomSearchState
  ) -> tuple[Parameters, RandomSearchState]:
    if value.ndim > 0:
      best = jnp.argmin(value)
      value = value[best]
      parameters = jax.tree_util.tree_map(lambda x: x[best], parameters)

    improved = (value < state.value)

    updated_parameters = jax.tree_util.tree_map(
      lambda current, proposed: jnp.where(improved, proposed, current),
      state.parameters, parameters
    )

    updated_value = jnp.minimum(state.value, value)

    return updated_parameters, RandomSearchState(
      parameters=updated_parameters,
      value=updated_value
    )

class LRS(RandomSearch):
  def __init__(self, learning_rate=1e-3):
    """
    Local random search:
    - applies a normal perturbation to the current estimate;
    - selects the best candidate among the current estimate and the perturbed parameters.

    :param learning_rate: standard deviation of perturbation noise.
    """
    self.learning_rate = learning_rate

  def propose(self, rng: jax.Array, state: RandomSearchState, batch: tuple[int, ...] = ()) -> Parameters:
    from .. import utils

    return jax.tree_util.tree_map(
      lambda k, x: x + self.learning_rate * jax.random.normal(k, shape=(*batch, *x.shape), dtype=x.dtype),
      utils.rng.split_rng(rng, state.parameters), state.parameters
    )

class GRS(RandomSearch):
  def __init__(self, bounds):
    """
    Global random search, which generates proposals within the specified bounds.
    """
    lower, upper = bounds
    self.lower = lower

    if isinstance(lower, (float, int)) and isinstance(upper, (float, int)):
      self.delta = upper - lower
    else:
      self.delta = jax.tree_util.tree_map(lambda l, u: u - l, lower, upper)

  def propose(self, rng: jax.Array, state: RandomSearchState, batch: tuple[int, ...]=()) -> Parameters:
    from .. import utils

    if isinstance(self.lower, (float, int)) and isinstance(self.delta, (float, int)):
      return jax.tree_util.tree_map(
        lambda k, x: jax.random.uniform(k, shape=(*batch, *x.shape), dtype=x.dtype) * self.delta + self.lower,
        utils.rng.split_rng(rng, state.parameters), state.parameters
      )

    else:
      return jax.tree_util.tree_map(
        lambda k, x, l, d: jax.random.uniform(k, shape=(*batch, *x.shape), dtype=x.dtype) * d + l,
        utils.rng.split_rng(rng, state.parameters), state.parameters, self.lower, self.delta
      )


MRSState = namedtuple('MomentumRandomSearchState', ['parameters', 'value', 'momentum'])

class MRS(BlackBoxOptimizer):
  OptimizerState = MRSState

  def __init__(self, learning_rate: float=1e-2, rho: float=0.9):
    """
    Local random search with momentum: the search direction is shifted by the momentum, all proposals contribute to
    the momentum:
    m[t + 1] = rho * m[t] + (1 - rho) * (sum_i proposal_i * (1 if value_i < current else -1))

    :param learning_rate: scale of perturbations;
    :param rho: exponential averaging coefficient.
    """
    self.learning_rate = learning_rate
    self.rho = rho

  def initial_state(self, parameters: Parameters) -> MRSState:
    return MRSState(
      parameters=parameters,
      ### as the value is unknown
      value=jnp.inf,
      momentum=jax.tree_util.tree_map(jnp.zeros_like, parameters),
    )

  def propose(self, rng: jax.Array, state: MRSState, batch: tuple[int, ...]=()) -> Parameters:
    from .. import utils

    return jax.tree_util.tree_map(
      lambda k, x, m: x + self.learning_rate * jax.random.normal(k, shape=(*batch, *x.shape), dtype=x.dtype) + m,
      utils.rng.split_rng(rng, state.parameters), state.parameters, state.momentum
    )

  def __call__(
    self, parameters: Parameters, value: Union[float, jax.numpy.ndarray], state: MRSState
  ) -> tuple[Parameters, MRSState]:
    from .. import utils

    if value.ndim > 0:
      better = jnp.where(value < state.value, jnp.ones_like(value), -jnp.ones_like(value))

      momentum_updated = jax.tree_util.tree_map(
        lambda x, m, p: self.rho * m + (1 - self.rho) * jnp.mean(utils.array.left_broadcast(better, p) * (p - x)),
        state.parameters, state.momentum, parameters
      )

      best = jnp.argmin(value)
      value = value[best]
      parameters = jax.tree_util.tree_map(lambda x: x[best], parameters)

    else:
      better = jnp.where(value < state.value, 1, -1)
      momentum_updated = jax.tree_util.tree_map(
        lambda x, m, p: self.rho * m + (1 - self.rho) * better * (p - x),
        state.parameters, state.momentum, parameters
      )


    improved = (value < state.value)

    updated_parameters = jax.tree_util.tree_map(
      lambda current, proposed: jnp.where(improved, proposed, current),
      state.parameters, parameters
    )

    updated_value = jnp.minimum(state.value, value)

    return updated_parameters, MRSState(
      parameters=updated_parameters,
      momentum=momentum_updated,
      value=updated_value
    )

class LinMRS(MRS):
  def __init__(self, learning_rate: float=1e-2, rho: float=0.9, alpha: Optional[float]=None):
    super().__init__(learning_rate, rho)
    self.alpha = alpha

  def __call__(
    self, parameters: Parameters, value: Union[float, jax.numpy.ndarray], state: MRSState
  ) -> tuple[Parameters, MRSState]:
    from .. import utils

    if value.ndim == 0:
      parameters = jax.tree_util.tree_map(lambda x: x[None], parameters)
      value = value[None]

    W, _ = utils.fit.quick_lin_fit(
      xs=parameters,
      fs=value,
      mu=jax.tree_util.tree_map(jnp.add, state.momentum, state.parameters),
      sigma=self.learning_rate,
      alpha=self.alpha
    )
    W_norm = jnp.sqrt(
      sum(
        jnp.sum(jnp.square(w))
        for w in jax.tree_util.tree_leaves(W)
      )
    )
    W_normed = jax.tree_util.tree_map(lambda x: x / W_norm, W)

    momentum_updated = jax.tree_util.tree_map(
      lambda m, w: self.rho * m + (1 - self.rho) * self.learning_rate * w,
      state.momentum, W_normed
    )

    best = jnp.argmin(value)
    value = value[best]
    parameters = jax.tree_util.tree_map(lambda x: x[best], parameters)

    improved = (value < state.value)

    updated_parameters = jax.tree_util.tree_map(
      lambda current, proposed: jnp.where(improved, proposed, current),
      state.parameters, parameters
    )

    updated_value = jnp.minimum(state.value, value)

    return updated_parameters, MRSState(
      parameters=updated_parameters,
      momentum=momentum_updated,
      value=updated_value
    )

DMRSState = namedtuple('DMRSState', ['parameters', 'value', 'momentum'])

class DMRS(BlackBoxOptimizer):
  OptimizerState = DMRSState

  def __init__(self, learning_rate=1e-2, rho=0.9):
    """
    Similar to local random search with momentum but, instead of just shifting the search distribution,
    DMRS does the following:
    - shifts the distribution by the momentum;
    - rotates the distribution such that the component is along the momentum;
    - stretches the distribution such that std along the main component matches norm of the momentum;
    - shrinks std along other components such that the determinant of the covariance matrix is approximately constant.

    :param learning_rate: the scale of the search distribution for zero momentum;
    :param rho: exponential averaging coefficient.
    """
    self.learning_rate = learning_rate
    self.rho = rho

  def initial_state(self, parameters: Parameters) -> DMRSState:
    return DMRSState(
      parameters=parameters,
      ### as the value is unknown
      value=jnp.inf,
      momentum=jax.tree_util.tree_map(jnp.zeros_like, parameters),
    )

  def propose(self, rng: jax.Array, state: DMRSState, batch: tuple[int, ...]=()) -> Parameters:
    from .. import utils
    n = sum(p.size for p in jax.tree_util.tree_leaves(state.parameters))

    def norm(tree):
      return jnp.sqrt(sum(
        jnp.sum(jnp.square(x))
        for x in jax.tree_util.tree_leaves(tree)
      ))

    mnorm = norm(state.momentum)

    sigma_r = jnp.exp(
      (n * jnp.log(self.learning_rate) - jnp.log(mnorm + self.learning_rate)) / (n - 1)
    )

    key1, key2 = jax.random.split(rng, num=2)

    eps_m = jax.random.normal(key2, shape=(*batch, ))

    return jax.tree_util.tree_map(
      lambda x, m, k1, k2: x + \
                           sigma_r * jax.random.normal(k1, shape=(*batch, *x.shape)) + \
                           m * (1 + utils.array.left_broadcast(eps_m, x)),
      state.parameters, state.momentum,
      utils.rng.split_rng(key1, state.parameters), utils.rng.split_rng(key2, state.parameters)
    )

  def __call__(
    self, parameters: Parameters, value: Union[float, jax.numpy.ndarray], state: DMRSState
  ) -> tuple[Parameters, DMRSState]:
    from .. import utils

    if value.ndim > 0:
      better = jnp.where(value < state.value, jnp.ones_like(value), -jnp.ones_like(value))

      momentum_updated = jax.tree_util.tree_map(
        lambda x, m, p: self.rho * m + (1 - self.rho) * jnp.mean(utils.array.left_broadcast(better, p) * (p - x)),
        state.parameters, state.momentum, parameters
      )

      best = jnp.argmin(value)
      value = value[best]
      parameters = jax.tree_util.tree_map(lambda x: x[best], parameters)

    else:
      better = jnp.where(value < state.value, 1, -1)
      momentum_updated = jax.tree_util.tree_map(
        lambda x, m, p: self.rho * m + (1 - self.rho) * better * (p - x),
        state.parameters, state.momentum, parameters
      )

    improved = (value < state.value)

    updated_parameters = jax.tree_util.tree_map(
      lambda current, proposed: jnp.where(improved, proposed, current),
      state.parameters, parameters
    )

    updated_value = jnp.minimum(state.value, value)

    return updated_parameters, DMRSState(
      parameters=updated_parameters,
      momentum=momentum_updated,
      value=updated_value
    )


RSSState = namedtuple('RSSState', ['parameters', 'value', 'momentum'])

class RSS(BlackBoxOptimizer):
  OptimizerState = RSSState

  def __init__(self, learning_rate=1e-2, rho=None):
    """
    Random subspace search.

    :param learning_rate: the scale of the search distribution for zero momentum;
    :param rho: exponential averaging coefficient.
    """
    self.learning_rate = learning_rate
    self.rho = rho

  def initial_state(self, parameters: Parameters) -> DMRSState:
    if self.rho is None:
      momentum = None
    else:
      momentum = jax.tree_util.tree_map(jnp.zeros_like, parameters)

    return RSSState(
      parameters=parameters,
      ### as the value is unknown
      value=jnp.inf,
      momentum=momentum,
    )

  def propose(self, rng: jax.Array, state: RSSState, batch: tuple[int, ...]=()) -> Parameters:
    from .. import utils
    key_eps, key_m = jax.random.split(rng, num=2)

    eps = jax.random.normal(key_eps, shape=batch)

    if state.momentum is None:
      search_direction = jax.tree_util.tree_map(
        lambda k, x: self.learning_rate * jax.random.normal(k, shape=x.shape),
        utils.rng.split_rng(key_m, state.parameters), state.parameters
      )
    else:
      search_direction = jax.tree_util.tree_map(
        lambda k, x, m: self.learning_rate * jax.random.normal(k, shape=x.shape) + m,
        utils.rng.split_rng(key_m, state.parameters), state.parameters, state.momentum
      )

    proposal = jax.tree_util.tree_map(
      lambda x, s: x + utils.array.left_broadcast(eps, eps.ndim + s.ndim) * s,
      state.parameters, search_direction
    )

    return proposal

  def __call__(
    self, parameters: Parameters, value: Union[float, jax.numpy.ndarray], state: RSSState
  ) -> tuple[Parameters, RSSState]:
    from .. import utils

    if value.ndim > 0:
      better = jnp.where(value < state.value, jnp.ones_like(value), -jnp.ones_like(value))

      if self.rho is None:
        momentum_updated = None
      else:
        momentum_updated = jax.tree_util.tree_map(
          lambda x, m, p: self.rho * m + (1 - self.rho) * jnp.mean(utils.array.left_broadcast(better, p) * (p - x)),
          state.parameters, state.momentum, parameters
        )

      best = jnp.argmin(value)
      value = value[best]
      parameters = jax.tree_util.tree_map(lambda x: x[best], parameters)

    else:
      better = jnp.where(value < state.value, 1, -1)

      if self.rho is None:
        momentum_updated = None
      else:
        momentum_updated = jax.tree_util.tree_map(
          lambda x, m, p: self.rho * m + (1 - self.rho) * better * (p - x),
          state.parameters, state.momentum, parameters
        )

    improved = (value < state.value)

    updated_parameters = jax.tree_util.tree_map(
      lambda current, proposed: jnp.where(improved, proposed, current),
      state.parameters, parameters
    )

    updated_value = jnp.minimum(state.value, value)

    return updated_parameters, RSSState(
      parameters=updated_parameters,
      momentum=momentum_updated,
      value=updated_value
    )