"""
Ziyin, L., Wang, Z. T., & Ueda, M. (2020).
LaProp: Separating momentum and adaptivity in adam. arXiv preprint arXiv:2002.04839.

https://arxiv.org/abs/2002.04839
"""

import jax
import jax.numpy as jnp
from collections import namedtuple

from .meta import GradientOptimizer, Parameters

__all__ = [
  'laprop',
]

LaPropState = namedtuple(
  'LaPropState',
  ['first_momentum', 'second_momentum', 'effective_mu', 'effective_nu']
)

class laprop(GradientOptimizer):
  State = LaPropState

  def __init__(self, learning_rate=1e-3, mu=0.9, nu=0.98, eps=1e-8):
    super(laprop, self).__init__()
    self.learning_rate = learning_rate
    self.mu = mu
    self.nu = nu

    self.eps = eps

  def initial_state(self, parameters: Parameters) -> LaPropState:
    from .. import utils
    dtype = utils.dtype.get_common_dtype(parameters)

    return LaPropState(
      first_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      second_momentum=jax.tree_util.tree_map(jax.numpy.zeros_like, parameters),
      effective_mu=jnp.ones(shape=(), dtype=dtype),
      effective_nu=jnp.ones(shape=(), dtype=dtype),
    )

  def __call__(
    self, parameters: Parameters, gradient: Parameters, state: LaPropState
  ) -> tuple[Parameters, LaPropState]:
    effective_mu = state.effective_mu * self.mu
    effective_nu = state.effective_nu * self.nu

    second_momentum_updated = jax.tree_util.tree_map(
      lambda m, g: self.nu * m + (1 - self.nu) * jnp.square(g),
      state.second_momentum, gradient
    )

    corrected_second_momentum = jax.tree_util.tree_map(
      lambda m: m * (1 - effective_nu),
      second_momentum_updated
    )

    first_momentum_updated = jax.tree_util.tree_map(
      lambda v, g, corr_m: self.mu * v + (1 - self.mu) * g / jnp.sqrt(corr_m + self.eps),
      state.first_momentum, gradient, corrected_second_momentum
    )

    corrected_momentum = jax.tree_util.tree_map(
      lambda m: m * (1 - effective_mu),
      first_momentum_updated
    )

    updated_parameters = jax.tree_util.tree_map(
      lambda x, v: x - self.learning_rate * v,
      parameters, corrected_momentum,
    )

    return updated_parameters, LaPropState(
      first_momentum=first_momentum_updated,
      second_momentum=second_momentum_updated,
      effective_mu=effective_mu,
      effective_nu=effective_nu
    )