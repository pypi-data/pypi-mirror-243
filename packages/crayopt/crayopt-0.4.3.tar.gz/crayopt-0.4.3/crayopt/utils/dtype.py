import jax

__all__ = [
  'get_common_dtype'
]

def get_common_dtype(parameters) -> jax.numpy.dtype:
  if hasattr(parameters, 'dtype'):
    return parameters.dtype
  else:
    *_, most_precise_dtype = sorted(
      (x.dtype for x in jax.tree_util.tree_leaves(parameters) if x.dtype.kind == 'f'),
      key=lambda d: d.itemsize
    )

    return most_precise_dtype



