from typing import Union

import jax
import jax.numpy as jnp

__all__ = [
  'left_broadcast'
]

def left_broadcast(x: jnp.ndarray, target: Union[int, tuple[int, ...], jnp.ndarray]):
  """
  Numpy and jax.numpy match dimensions starting with the last ones ("right broadcast"), e.g.,
  a binary operation on arrays with shapes (n, m) and (k, l, n, m) broadcasts the first operator to (1, 1, n, m).

  This function broadcasts an array `x` starting with the first dimensions ("from the left"), e.g.,
  an array with shape (n, m) and the target shape (n, m, k, l) is broadcasted to (n, m, 1, 1).

  :arg x: an array to broadcast;
  :arg target: either integer, number of dimensions, or tuple of integers, the target shape, or an array
    of the target shape.

  :returns: `x` broadcasted "from the left" to match `target`.
  """

  if hasattr(target, 'ndim'):
    ndim = getattr(target, 'ndim')
  elif isinstance(target, int):
    ndim = target
  else:
    ndim = len(target)

  broadcast = (
    *(slice(None, None, None) for _ in x.shape),
    *(None for _ in range(x.ndim, ndim))
  )

  return x[broadcast]
