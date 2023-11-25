import jax

__all__ = [
  'split_rng'
]

def split_rng(rng, x):
  """
  Splits `rng` into RNG keys for each tensor in `x`.
  The result has the same structure as `x` (as interpreted by `jax.tree_utils`).
  """

  x_flat, treedef = jax.tree_util.tree_flatten(x)
  keys = jax.random.split(rng, num=len(x_flat))
  return jax.tree_util.tree_unflatten(treedef, keys)