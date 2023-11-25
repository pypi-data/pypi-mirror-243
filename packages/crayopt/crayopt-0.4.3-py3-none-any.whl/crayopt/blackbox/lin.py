from typing import Union, Optional
import jax
import jax.numpy as jnp

from .meta import BlackBoxOptimizer, Parameters

from ..gradient import GradientOptimizer, adam
from .. import utils

from collections import namedtuple

__all__ = [
  'LinGrad', 'QuadGrad', 'KernelGradState'
]

KernelGradState = namedtuple('KernelGradState', ['mu', 'gradient_state'])

class KernelGrad(BlackBoxOptimizer):
  State = KernelGradState

  def fit(self, xs, fs, mu):
    raise NotImplementedError()

  def predict(self, xs, params):
    raise NotImplementedError()

  def __init__(self, sigma: float, gradient: GradientOptimizer = adam(), alpha: Optional[float] = None):
    self.sigma = sigma
    self.gradient = gradient
    self.alpha = alpha

    def encode(xs, mu):
      return jax.tree_util.tree_map(
        lambda x, m: (x - m) / sigma,
        xs, mu
      )

    def decode(eps, mu):
      return jax.tree_util.tree_map(
        lambda e, m: e * sigma + m,
        eps, mu
      )

    def c(eps, mu, params):
      xs = decode(eps, mu)
      return self.predict(xs, params)

    self.c = c

    def grad(xs, fs, mu):
      params = self.fit(xs, fs, mu)
      eps = encode(xs, mu)
      return jax.grad(
        lambda e, m, p: jnp.mean(c(e, m, p)),
        argnums=1
      )(eps, mu, params)

    self.grad = grad

    super().__init__()

  def initial_state(self, parameters: Parameters) -> KernelGradState:
    mu = jax.tree_util.tree_map(lambda x: x, parameters)

    return KernelGradState(mu, self.gradient.initial_state(mu))

  def propose(self, rng: jax.Array, state: KernelGradState, batch: tuple[int, ...] = ()) -> Parameters:
    return jax.tree_util.tree_map(
      lambda k, m: self.sigma * jax.random.normal(k, shape=(*batch, *m.shape)) + m,
      utils.rng.split_rng(rng, state.mu),
      state.mu
    )

  def __call__(
    self, parameters: Parameters, value: Union[float, jax.numpy.ndarray], state: KernelGradState
  ) -> tuple[Parameters, KernelGradState]:
    grad_mu = self.grad(parameters, value, state.mu)
    mu_updated, gradient_state_updated = self.gradient(state.mu, grad_mu, state.gradient_state)
    return mu_updated, KernelGradState(mu_updated, gradient_state_updated)

class LinGrad(KernelGrad):
  def fit(self, xs, fs, mu):
    return utils.fit.quick_lin_fit(xs, fs, mu, self.sigma)

  def predict(self, xs, params):
    return utils.fit.lin_predict(xs, *params)

class QuadGrad(KernelGrad):
  def fit(self, xs, fs, mu):
    return utils.fit.lstsq_quad_fit(xs, fs, mu, self.sigma)

  def predict(self, xs, params):
    return utils.fit.quad_predict(xs, *params)