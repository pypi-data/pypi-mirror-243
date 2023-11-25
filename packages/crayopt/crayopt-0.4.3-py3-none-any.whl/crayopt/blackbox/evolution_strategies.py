from typing import Union
from collections import namedtuple

import jax
import jax.numpy as jnp

from ..gradient import GradientOptimizer, adam
from .meta import BlackBoxOptimizer, Parameters
from .. import utils

__all__ = [
  'REINFORCE', 'REINFORCEState',
  'SES', 'SESState',
  'SNES', 'SNESState'
]

REINFORCEState = namedtuple('REINFORCEState', ['mu', 'momentum', 'gradient_state'])

class REINFORCE(BlackBoxOptimizer):
  """
  Separable Evolution Strategies with parametrization close to the natural:
      mu = exp(0.5 * log_sigma) * normalized_mu
      sigma = exp(0.5 * log_sigma)
  i.e.:
      ||d normalized_mu|| + || d log_sigma || ~= KL(P' || P)
  where: P, P' --- original and modified distributions.
  """
  OptimizerState = REINFORCEState

  def __init__(self, sigma: float, rho: float=0.9, gradient: GradientOptimizer=adam()):
    self.rho = rho
    self.sigma = sigma

    def J(mu, xs, fs):
      log_ps = jax.tree_util.tree_map(
        lambda m, x: jnp.sum(
          -0.5 * jnp.square((x - m) / self.sigma),
          axis=range(x.ndim - m.ndim, x.ndim)
        ),
        mu, xs
      )

      log_p = sum(jax.tree_util.tree_leaves(log_ps))

      return jnp.mean(log_p * fs)

    self.grad_J = jax.grad(J, argnums=0)

    self.gradient = gradient

    super().__init__()

  def initial_state(self, parameters: Parameters) -> REINFORCEState:
    dtype = utils.dtype.get_common_dtype(parameters)

    mu = jax.tree_util.tree_map(lambda x: x, parameters)
    momentum = jnp.zeros(shape=(), dtype=dtype)

    grad_state = self.gradient.initial_state(mu)

    return REINFORCEState(mu, momentum, grad_state)

  def propose(self, rng: jax.Array, state: REINFORCEState, batch: tuple[int, ...]=()) -> Parameters:
    return jax.tree_util.tree_map(
      lambda k, m: jax.random.normal(k, shape=(*batch, *m.shape)) * self.sigma + m,
      utils.rng.split_rng(rng, state.mu),
      state.mu
    )

  def __call__(
    self, proposal: Parameters, values: Union[float, jax.numpy.ndarray], state: REINFORCEState
  ) -> tuple[Parameters, REINFORCEState]:
    momentum_updated = self.rho * state.momentum + (1 - self.rho) * jnp.mean(values)

    grad = self.grad_J(state.mu, proposal, values - momentum_updated)
    mu_updated, gradient_state_updated = self.gradient(state.mu, grad, state.gradient_state)

    return mu_updated, REINFORCEState(mu_updated, momentum_updated, gradient_state_updated)


SESState = namedtuple('SESState', ['normalized_mu', 'log_sigma', 'momentum', 'grad_state'])

class SES(BlackBoxOptimizer):
  """
  Separable Evolution Strategies with parametrization close to the natural:
      mu = exp(0.5 * log_sigma) * normalized_mu
      sigma = exp(0.5 * log_sigma)
  i.e.:
      ||d normalized_mu|| + || d log_sigma || ~= KL(P' || P)
  where: P, P' --- original and modified distributions.
  """
  OptimizerState = SESState

  @staticmethod
  def decode(normalized_mu, log_sigma):
    sigma = jax.tree_util.tree_map(
      lambda s: jnp.exp(0.5 * s),
      log_sigma
    )

    mu = jax.tree_util.tree_map(
      lambda nm, s: nm * s,
      normalized_mu, sigma
    )

    return mu, sigma

  @staticmethod
  def encode(mu, sigma):
    normalized_mu = jax.tree_util.tree_map(
      lambda m, s: m / s,
      mu, sigma
    )

    log_sigma = jax.tree_util.tree_map(
      lambda s: 2 * jnp.log(s),
      sigma
    )

    return normalized_mu, log_sigma

  def __init__(self, initial_sigma: float, rho: float=0.9, gradient: GradientOptimizer=adam()):
    self.rho = rho
    self.initial_sigma = initial_sigma

    def J(nmu, log_sigma, xs, fs):
      log_ps = jax.tree_util.tree_map(
        lambda nm, log_s, x: jnp.sum(
          -0.5 * (log_s + jnp.square(x * jnp.exp(-0.5 * log_s) - nm)),
          axis=range(x.ndim - nm.ndim, x.ndim)
        ),
        nmu, log_sigma, xs
      )

      log_p = sum(jax.tree_util.tree_leaves(log_ps))

      return jnp.mean(log_p * fs)

    self.grad_J = jax.grad(J, argnums=(0, 1))

    self.gradient = gradient

    super().__init__()

  def initial_state(self, parameters: Parameters) -> SESState:
    dtype = utils.dtype.get_common_dtype(parameters)

    normalized_mu = jax.tree_util.tree_map(
      lambda x: x / self.initial_sigma,
      parameters,
    )

    log_sigma = jax.tree_util.tree_map(
      lambda x: 2 * jnp.log(self.initial_sigma) * jnp.ones_like(x),
      parameters
    )
    momentum = jnp.zeros(shape=(), dtype=dtype)

    grad_state = self.gradient.initial_state((normalized_mu, log_sigma))

    return SESState(normalized_mu, log_sigma, momentum, grad_state)

  def propose(self, rng: jax.Array, state: SESState, batch: tuple[int, ...]=()) -> Parameters:
    def sample(key, nm, log_s):
      eps = jax.random.normal(key, shape=(*batch, *nm.shape))
      s = jnp.exp(0.5 * log_s)
      m = s * nm

      return eps * s + m

    return jax.tree_util.tree_map(
      sample,
      utils.rng.split_rng(rng, state.normalized_mu),
      state.normalized_mu,
      state.log_sigma
    )

  def __call__(
    self, proposal: Parameters, values: Union[float, jax.numpy.ndarray], state: SESState
  ) -> tuple[Parameters, SESState]:
    momentum_updated = self.rho * state.momentum + (1 - self.rho) * jnp.mean(values)

    grad = self.grad_J(state.normalized_mu, state.log_sigma, proposal, values - momentum_updated)
    (mu_updated, log_sigma_updated), gradient_state_updated = self.gradient(
      (state.normalized_mu, state.log_sigma),
      grad,
      state.grad_state
    )

    estimate = jax.tree_util.tree_map(
      lambda m, log_s: m * jnp.exp(0.5 * log_s),
      mu_updated, log_sigma_updated
    )

    return estimate, SESState(mu_updated, log_sigma_updated, momentum_updated, gradient_state_updated)

SNESState = namedtuple('ESState', ['mu', 'sigma', 'momentum'])

class SNES(BlackBoxOptimizer):
  OptimizerState = SNESState

  def __init__(self, learning_rate: float, sigma0: float, rho: float=0.9, *, learning_rate_sigma: float=None):
    self.learning_rate = learning_rate
    if learning_rate_sigma is None:
      self.learning_rate_sigma = learning_rate
    else:
      self.learning_rate_sigma = learning_rate_sigma

    self.rho = rho
    self.sigma0 = sigma0

    super().__init__()

  def initial_state(self, parameters: Parameters) -> Parameters:
    dtype = utils.dtype.get_common_dtype(parameters)

    mu = parameters
    sigma = jax.tree_util.tree_map(
      lambda x: self.sigma0 * jnp.ones_like(x),
      parameters
    )
    momentum = jnp.zeros(shape=(), dtype=dtype)

    return SNESState(mu, sigma, momentum)

  def propose(self, rng: jax.Array, state: SNESState, batch: tuple[int, ...]=()) -> Parameters:
    eps: Parameters = jax.tree_util.tree_map(
      lambda k, m, s: s * jax.random.normal(k, shape=(*batch, *m.shape)) + m,
      utils.rng.split_rng(rng, state.mu),
      state.mu,
      state.sigma
    )

    return eps

  def __call__(self, parameters: Parameters, values: jax.numpy.ndarray, state: SNESState) -> tuple[Parameters, SNESState]:
    momentum_updated = self.rho * state.momentum + (1 - self.rho) * jnp.mean(values)

    fs = jnp.argsort(values.ravel()).reshape(values.shape)
    fs = fs / fs.size - 0.5

    eps = jax.tree_util.tree_map(
      lambda x, m, s: (x - m) / s,
      parameters, state.mu, state.sigma
    )

    grad_mu = jax.tree_util.tree_map(
      lambda e: jnp.mean(
        e * utils.array.left_broadcast(fs, e),
        axis=range(fs.ndim)
      ),
      eps
    )

    grad_sigma = jax.tree_util.tree_map(
      lambda e: jnp.mean(
        (jnp.square(e) - 1) * utils.array.left_broadcast(fs, e),
        axis=range(fs.ndim)
      ),
      eps
    )

    mu_updated = jax.tree_util.tree_map(
      lambda m, gm, s: m - self.learning_rate * s * gm,
      state.mu, grad_mu, state.sigma
    )

    sigma_updated = jax.tree_util.tree_map(
      lambda s, gs: s * jnp.exp(-0.5 * self.learning_rate_sigma * gs),
      state.sigma, grad_sigma
    )

    return mu_updated, SNESState(mu_updated, sigma_updated, momentum_updated)