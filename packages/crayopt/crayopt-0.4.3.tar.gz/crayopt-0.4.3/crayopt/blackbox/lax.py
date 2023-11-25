from typing import Union, Optional
from collections import namedtuple

import jax
import jax.numpy as jnp

from ..gradient import GradientOptimizer, adam
from .meta import BlackBoxOptimizer, Parameters
from .. import utils

__all__ = [
  'LAX', 'LAXState',
  'LinLAX', 'QuadLAX', 'FastLinLAX', 'FastQuadLAX'
]

LAXState = namedtuple('LAXState', ['mu', 'gradient_state', 'rscore'])

class LAX(BlackBoxOptimizer):
  State = LAXState

  def fit(self, xs, fs, mu):
    raise NotImplementedError()

  def predict(self, xs, params):
    raise NotImplementedError()

  def __init__(self, sigma: float, gradient: GradientOptimizer=adam()):
    self.sigma = sigma
    self.gradient = gradient

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

    def value_and_grad(eps, mu, params):
      value = c(eps, mu, params)
      grad = jax.grad(
        lambda e, m, p: jnp.mean(c(e, m, p)),
        argnums=1
      )(eps, mu, params)

      return value, grad

    self.value_and_grad_c = value_and_grad

    def J(xs, fs, mu):
      log_ps = jax.tree_util.tree_map(
        lambda x, m: jnp.sum(
          -0.5 * jnp.square((x - m) / sigma),
          axis=range(x.ndim - m.ndim, x.ndim)
        ),
        xs, mu
      )

      log_p = sum(jax.tree_util.tree_leaves(log_ps))

      return jnp.mean(log_p * fs)

    self.grad_J = jax.grad(J, argnums=2)

    def lax_grad(xs, fs, mu):
      params = self.fit(xs, fs, mu)
      eps = encode(xs, mu)

      ps, grad_c_mu = self.value_and_grad_c(eps, mu, params)
      grad_J_mu = self.grad_J(xs, fs - ps, mu)

      grad_mu = jax.tree_util.tree_map(jnp.add, grad_c_mu, grad_J_mu)

      rscore = jnp.mean(jnp.square(fs - ps)) / jnp.mean(jnp.square(fs - jnp.mean(fs)))

      return grad_mu, rscore

    self.lax_grad = lax_grad

    super().__init__()

  def initial_state(self, parameters: Parameters) -> LAXState:
    mu = jax.tree_util.tree_map(lambda x: x, parameters)

    return LAXState(mu, self.gradient.initial_state(mu), rscore=0.0)

  def propose(self, rng: jax.Array, state: LAXState, batch: tuple[int, ...]=()) -> Parameters:
    return jax.tree_util.tree_map(
      lambda k, m: self.sigma * jax.random.normal(k, shape=(*batch, *m.shape)) + m,
      utils.rng.split_rng(rng, state.mu),
      state.mu
    )

  def __call__(
    self, parameters: Parameters, value: Union[float, jax.numpy.ndarray], state: LAXState
  ) -> tuple[Parameters, LAXState]:
    grad_mu, rscore = self.lax_grad(parameters, value, state.mu)

    mu_updated, gradient_state_updated = self.gradient(state.mu, grad_mu, state.gradient_state)

    return mu_updated, LAXState(mu_updated, gradient_state_updated, rscore)


class LinLAX(LAX):
  def fit(self, xs, fs, mu):
    from .. import utils
    return utils.fit.lstsq_fit(xs, fs, mu, self.sigma)

  def predict(self, xs, params):
    from .. import utils
    W, b = params
    return utils.fit.lin_predict(xs, W, b)

class FastLinLAX(LAX):
  def __init__(self, sigma: float, gradient: GradientOptimizer=adam(), alpha: Optional[float]=None):
    super().__init__(sigma, gradient)
    self.alpha = alpha

  def fit(self, xs, fs, mu):
    from .. import utils
    return utils.fit.quick_lin_fit(xs, fs, mu, self.sigma, alpha=self.alpha)

  def predict(self, xs, params):
    from .. import utils
    W, b = params
    return utils.fit.lin_predict(xs, W, b)

class QuadLAX(LAX):
  def fit(self, xs, fs, mu):
    from .. import utils
    return utils.fit.lstsq_quad_fit(xs, fs, mu, self.sigma)

  def predict(self, xs, params):
    from .. import utils
    return utils.fit.quad_predict(xs, *params)

class FastQuadLAX(QuadLAX):
  pass
