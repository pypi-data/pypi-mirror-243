from typing import Optional
from functools import partial

import numpy as np

import jax
import jax.numpy as jnp

__all__ = [
  'iterate',
  'batched'
]

def make_buffer(step_results, batch_dim):
  shapes = [
    getattr(res, 'shape', tuple())
    for res in step_results
  ]
  return [
    np.zeros(shape=batch_dim + shape)
    for shape in shapes
  ]

def _split_first(values, n):
  if isinstance(values, (tuple, list)):
    return values[:n], values[n:], False
  elif n == 1:
    return (values, ), (), True
  elif n == 0:
    return (), (values, ), True
  else:
    raise ValueError('Can not split value %s at n=%d' % (values, n))

def _split(values, n, single):
  if not single:
    return values[:n], values[n:]
  elif n == 1:
    return (values, ), ()
  elif n == 0:
    return (), (values, )
  else:
    raise ValueError('Can not split value %s at n=%d' % (values, n))

def get_mapping(step, validation_functions):
  import inspect

  if len(validation_functions) == 0:
    return ()

  state_name_mapping = {p: i for i, p in enumerate(inspect.signature(step).parameters)}

  validation_mapping = list()
  for f in validation_functions:
    try:
      validation_mapping.append(
        tuple(state_name_mapping[p] for p in inspect.signature(f).parameters)
      )
    except:
      validation_mapping.append(None)

  return tuple(validation_mapping)

def apply_with_mapping(f, values, mapping):
  if mapping is None:
    return f(*values)
  else:
    return f(*(values[i] for i in mapping))

def validate(validation_functions, values, validation_mapping):
  result = list()
  for f, mapping in zip(validation_functions, validation_mapping):
    res = apply_with_mapping(f, values, mapping)

    if isinstance(res, (tuple, list)):
      result.extend(res)
    else:
      result.append(res)

  return tuple(result)

def _iterate_1D(step, initial_values, n_iterations, progress=None):
  if progress is not None:
    pbar = progress(total=n_iterations)
    pbar_inc = pbar.update
    pbar_close = pbar.close
  else:
    pbar_inc = lambda: None
    pbar_close = lambda: None

  n_state = len(initial_values)
  state = initial_values

  state, aux, single_output = _split_first(step(*state), n_state)
  n_aux = len(aux)
  aux_buffers = make_buffer(aux, (n_iterations,))

  pbar_inc()

  for k in range(n_aux):
    aux_buffers[k][0] = aux[k]

  for j in range(1, n_iterations):
    state, aux = _split(step(*state), n_state, single_output)
    pbar_inc()

    for k in range(n_aux):
      aux_buffers[k][j] = aux[k]

  pbar_close()

  if single_output:
    if n_state == 0:
      assert n_aux == 1
      return aux_buffers[0]
    else:
      assert n_aux == 0 and n_state == 1
      return state[0]
  else:
    return *state, *aux_buffers

def _iterate_2D(step, initial_values, validation_functions, n_iterations, n_epoches, progress=None):
  if progress is not None:
    pbar = progress(total=n_epoches)
    pbar_inc = pbar.update
    pbar_close = pbar.close

    pbar_secondary = progress(total=n_iterations, leave=False)
    pbar_inc_secondary = pbar_secondary.update
    pbar_close_secondary = pbar_secondary.close
    pbar_reset_secondary = pbar_secondary.reset
  else:
    pbar_inc = lambda: None
    pbar_close = lambda: None
    pbar_inc_secondary = lambda: None
    pbar_close_secondary = lambda: None
    pbar_reset_secondary = lambda: None

  validation_mapping = get_mapping(step, validation_functions)

  n_state = len(initial_values)
  state = initial_values

  state, aux, single_output = _split_first(step(*state), n_state)
  n_aux = len(aux)
  aux_buffers = make_buffer(aux, (n_epoches, n_iterations,))

  pbar_inc_secondary()

  ### collecting the first iteration
  for k in range(n_aux):
    aux_buffers[k][0, 0] = aux[k]

  ### collecting the first epoch
  for j in range(1, n_iterations):
    state, aux = _split(step(*state), n_state, single_output)
    for k in range(n_aux):
      aux_buffers[k][0, j] = aux[k]

    pbar_inc_secondary()
  pbar_inc()

  val = validate(validation_functions, state, validation_mapping)
  n_val = len(val)
  val_buffers = make_buffer(val, (n_epoches, ))

  for k in range(n_val):
    val_buffers[k][0] = val[k]

  for i in range(1, n_epoches):
    pbar_reset_secondary()

    for j in range(n_iterations):
      state, aux = _split(step(*state), n_state, single_output)
      for k in range(n_aux):
        aux_buffers[k][i, j] = aux[k]

      pbar_inc_secondary()

    val = validate(validation_functions, state, validation_mapping)
    for k in range(n_val):
      val_buffers[k][i] = val[k]

    pbar_inc()

  pbar_close_secondary()
  pbar_close()

  if single_output and n_val == 0:
    if n_state == 0:
      assert n_aux == 1
      return aux_buffers[0]
    else:
      assert n_aux == 0 and n_state == 1
      return state[0]
  else:
    return *state, *aux_buffers, *val_buffers

class iterate(object):
  def __init__(self, step, epochs, iterations=None, *, progress=None, validation=None):
    self._step = step
    if iterations is None:
      self._n_epochs = None
      self._n_iterations = epochs
    else:
      self._n_epochs = epochs
      self._n_iterations = iterations

    self._progress = progress

    if validation is None:
      self._validation = list()
    else:
      assert self._n_epochs is not None, 'validation does not make sense for a iteration without epoches'
      self._validation = list(validation)

  def validate(self, *functions):
    assert self._n_epochs is not None, 'validation does not make sense for a iteration without epoches'
    return iterate(
      self._step, self._n_epochs, self._n_iterations,
      progress=self._progress,
      validation=[*self._validation, *functions]
    )

  def __call__(self, *initial_values):
    if self._n_epochs is None:
      assert len(self._validation) == 0

      return _iterate_1D(
        self._step, initial_values,
        self._n_iterations,
        progress=self._progress
      )
    else:
      return _iterate_2D(
        self._step, initial_values, self._validation,
        self._n_iterations, self._n_epochs,
        progress=self._progress
      )

@partial(jax.jit, static_argnums=(2, 3, 4))
def sample(key: jax.Array, xs, size: int, batch: int, axis: int=0):
  indx = jax.random.randint(key, minval=0, maxval=size, shape=(batch, ))
  return jax.tree_util.tree_map(
    lambda x: jnp.take(x, indx, axis=axis),
    xs
  )

def batched(rng, data, batch: int, epochs, iterations: Optional[int]=None, axis: int=0, *, progress=None):
  sizes = set(x.shape[axis] for x in jax.tree_util.tree_leaves(data))

  if len(sizes) > 1:
    raise ValueError(
      f'Size of the dataset is inconsistent along the axis {axis} ({list(sizes)})'
    )

  size, = sizes

  if iterations is None:
    iterations = max(size // batch, 1)

  if progress is not None:
    pbar = progress(total=epochs)
    pbar_inc = pbar.update
    pbar_close = pbar.close

    pbar_secondary = progress(total=iterations, leave=False)
    pbar_inc_secondary = pbar_secondary.update
    pbar_close_secondary = pbar_secondary.close
    pbar_reset_secondary = pbar_secondary.reset
  else:
    pbar_inc = lambda: None
    pbar_close = lambda: None
    pbar_inc_secondary = lambda: None
    pbar_close_secondary = lambda: None
    pbar_reset_secondary = lambda: None


  for i in range(epochs):
    pbar_reset_secondary()

    for j in range(iterations):
      rng, key = jax.random.split(rng, num=2)
      yield i, j, sample(key, data, size, batch, axis)
      pbar_inc_secondary()
    pbar_inc()

  pbar_close_secondary()
  pbar_close()

