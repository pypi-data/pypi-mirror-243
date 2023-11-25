import jax
import jax.numpy as jnp

import math

__all__ = [
  'tensor_pack',
  'tensor_unpack'
]


def tensor_pack(tree, batch_dimensions=(0, )):
  batch_dimensions = tuple(batch_dimensions)

  assert all(i in batch_dimensions for i in range(max(batch_dimensions) + 1)), 'batch dimensions must be consecutive'

  tree_flat, tree_def = jax.tree_util.tree_flatten(tree)

  original_shapes = tuple(
    tuple(x.shape[i] for i in range(x.ndim) if i not in batch_dimensions)
    for x in tree_flat
  )

  tree_mat = [
    x.reshape((
      *(x.shape[i] for i in batch_dimensions),
      math.prod(x.shape[i] for i in range(x.ndim) if i not in batch_dimensions)
    ))

    for x in tree_flat
  ]

  return jnp.concatenate(tree_mat, axis=-1), (tree_def, original_shapes)

def tensor_unpack(tensor_def, tensor):
  tree_def, original_shapes = tensor_def

  tree_mat = list()
  i = 0

  for original_shape in original_shapes:
    size = math.prod(original_shape)

    subtensor = tensor[..., i:(i + size)]
    tree_mat.append(
      subtensor.reshape(
        (*subtensor.shape[:-1], *original_shape)
      )
    )
    i += size

  return jax.tree_util.tree_unflatten(tree_def, tree_mat)