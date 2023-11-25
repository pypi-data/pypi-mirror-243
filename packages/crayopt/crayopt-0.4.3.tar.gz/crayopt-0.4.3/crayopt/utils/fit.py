import math

import jax
import jax.numpy as jnp

from . import tree, array

__all__ = [
  'lstsq_fit', 'quick_lin_fit', 'lin_predict',
  'lstsq_quad_fit', 'quad_predict'
]

def lin_normalize(xs, fs, mu, sigma):
  fs_m = jnp.mean(fs)
  fs_c = fs - fs_m

  xs_n = jax.tree_util.tree_map(lambda x, m: (x - m) / sigma, xs, mu)

  return xs_n, fs_c, fs_m

def lin_recover(W, b, mu, sigma, fs_m):
  W_r = jax.tree_util.tree_map(lambda w: w / sigma, W)

  b_r = b + fs_m - sum(
    jnp.sum(w_r * m) for w_r, m in zip(
      jax.tree_util.tree_leaves(W_r),
      jax.tree_util.tree_leaves(mu),
    )
  )

  return W_r, b_r

def lstsq_fit(xs, fs, mu=None, sigma=None):
  if mu is None:
    mu = jnp.mean(xs, axis=range(fs.ndim))

  if sigma is None:
    sigma = jnp.sqrt(jnp.mean(jnp.square(xs - mu)))

  xs_n, fs_c, fs_m = lin_normalize(xs, fs, mu, sigma)

  tensor, tensor_def = tree.tensor_pack(
    (xs_n, jnp.ones(shape=fs.shape)),
    batch_dimensions=range(fs.ndim)
  )

  M = tensor.reshape((fs.size, tensor.shape[-1]))

  weights, _, _, _ = jnp.linalg.lstsq(M, fs_c.ravel())
  W, offset = tree.tensor_unpack(tensor_def, weights)

  return lin_recover(W, offset, mu, sigma, fs_m)


def quick_lin_fit(xs, fs, mu, sigma, alpha=None):
  fs_m = jnp.mean(fs)

  if alpha is None:
    sqr_sigma = sigma * sigma
  else:
    sqr_sigma = sigma * sigma + alpha * alpha

  W = jax.tree_util.tree_map(
    lambda x, m: jnp.mean(
      (x - m) * array.left_broadcast(fs - fs_m, x),
      axis=range(fs.ndim)
    ) / sqr_sigma,
    xs, mu
  )

  b = fs_m - sum(
    jnp.sum(w * m) for w, m in zip(
      jax.tree_util.tree_leaves(W),
      jax.tree_util.tree_leaves(mu),
    )
  )

  return W, b

def lin_predict(xs, W, b):
  ps = jax.tree_util.tree_map(
    lambda x, w: jnp.sum(x * w, axis=range(x.ndim - w.ndim, x.ndim)),
    xs, W
  )

  return sum(jax.tree_util.tree_leaves(ps)) + b

def lstsq_quad_fit(xs, fs, mu=None, sigma=None):
  if mu is None:
    mu = jnp.mean(xs, axis=range(fs.ndim))

  if sigma is None:
    sigma = jnp.sqrt(jnp.mean(jnp.square(xs - mu)))

  fs_m = jnp.mean(fs)
  fs_c = fs - fs_m

  xs_n = jax.tree_util.tree_map(lambda x, m: (x - m) / sigma, xs, mu)
  xs_sqr_n = jax.tree_util.tree_map(lambda x: jnp.square(x) - 1, xs_n)

  tensor, tensor_def = tree.tensor_pack(
    (xs_sqr_n, xs_n, jnp.ones(shape=fs.shape)),
    batch_dimensions=range(fs.ndim)
  )

  M = tensor.reshape((fs.size, tensor.shape[-1]))

  weights, _, _, _ = jnp.linalg.lstsq(M, fs_c.ravel())
  W_sqr, W_lin, offset = tree.tensor_unpack(tensor_def, weights)

  W_sqr_r = jax.tree_util.tree_map(lambda w_sqr: w_sqr / (sigma * sigma), W_sqr)
  W_lin_r = jax.tree_util.tree_map(
    lambda w_sqr_r, w_lin, m: w_lin / sigma - 2 * w_sqr_r * m,
    W_sqr_r, W_lin, mu
  )

  b_sqr_correction = sum(
    jnp.sum(w_sqr_r * jnp.square(m)) - jnp.sum(w_sqr) for w_sqr_r, w_sqr, m in zip(
      jax.tree_util.tree_leaves(W_sqr_r),
      jax.tree_util.tree_leaves(W_sqr),
      jax.tree_util.tree_leaves(mu),
    )
  )

  b_lin_correction = -sum(
    jnp.sum(w_lin * m) / sigma for w_lin, m in zip(
      jax.tree_util.tree_leaves(W_lin),
      jax.tree_util.tree_leaves(mu),
    )
  )

  b = offset + fs_m + b_sqr_correction + b_lin_correction

  return W_sqr_r, W_lin_r, b

def quad_predict(xs, W_sqr, W_lin, b):
  ps = jax.tree_util.tree_map(
    lambda x, w_sqr, w_lin: \
      jnp.sum(jnp.square(x) * w_sqr, axis=range(x.ndim - w_sqr.ndim, x.ndim)) + \
        jnp.sum(x * w_lin, axis=range(x.ndim - w_lin.ndim, x.ndim)),

    xs, W_sqr, W_lin
  )

  return sum(jax.tree_util.tree_leaves(ps)) + b