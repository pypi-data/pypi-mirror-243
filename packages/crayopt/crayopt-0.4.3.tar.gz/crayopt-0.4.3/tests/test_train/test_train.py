import jax.random
import numpy as np

import crayopt


def test_iterate():
  tqdm = None
  import crayopt

  n_iter = 1024
  n_epoches = 33

  shape_iter = (n_iter, )
  shape_epoch = (n_epoches, n_iter, )

  def step():
    return 1

  aux = crayopt.train.iterate(step, n_iter, progress=tqdm)()
  assert not isinstance(aux, tuple)
  assert np.allclose(np.ones(shape=shape_iter), aux)

  aux = crayopt.train.iterate(step, n_epoches, n_iter, progress=tqdm)()
  assert not isinstance(aux, tuple)
  assert np.allclose(np.ones(shape=shape_epoch), aux)

  def step():
    return 1, np.array([2, 3])

  aux1, aux2 = crayopt.train.iterate(step, n_iter, progress=tqdm)()
  assert np.allclose(np.ones(shape=shape_iter), aux1)
  assert np.allclose(np.array([2, 3]) * np.ones(shape=shape_iter + (2, )), aux2)

  crayopt.train.iterate(step, n_epoches, n_iter, progress=tqdm)()
  assert np.allclose(np.ones(shape=shape_epoch), aux1)
  assert np.allclose(np.array([2, 3]) * np.ones(shape=shape_epoch + (2,)), aux2)

  def step(i):
    return i + 1

  result = crayopt.train.iterate(step, n_iter, progress=tqdm)(0)
  assert result == n_iter

  result = crayopt.train.iterate(step, n_epoches, n_iter, progress=tqdm)(0)
  assert result == n_iter * n_epoches

  def step(i):
    return i + 1, i + 1

  result, aux = crayopt.train.iterate(step, n_iter, progress=tqdm)(0)
  assert result == n_iter
  assert np.allclose(np.arange(n_iter) + 1, aux)

  result, aux = crayopt.train.iterate(step, n_epoches, n_iter, progress=tqdm)(0)
  assert result == n_iter * n_epoches
  assert np.allclose(
    np.arange(1, n_iter * n_epoches + 1).reshape(n_epoches, n_iter),
    aux
  )

  def step(i, j):
    return i + 1, j // 3

  result1, result2 = crayopt.train.iterate(step, n_epoches, n_iter, progress=tqdm)(0, 1)
  assert result1 == n_iter * n_epoches
  assert result2 == 0

  def step(i, j):
    return i + 1, j // 3, i + j // 3

  def f1(j):
    return j * 10

  def f2(i):
    return i * 100

  def f3(j, i):
    return j * 1000000 + i * 200

  result1, result2, aux, val1 = crayopt.train.iterate(step, n_epoches, n_iter, progress=tqdm).validate(f1)(0, 1)
  assert result1 == n_iter * n_epoches
  assert result2 == 0
  assert np.allclose(aux, np.arange(n_iter * n_epoches).reshape(n_epoches, n_iter))
  assert np.allclose(val1, np.zeros(n_epoches))

  result1, result2, aux, val1, val2, val3 = \
    crayopt.train.iterate(step, n_epoches, n_iter, progress=tqdm).validate(f1, f2, f3)(0, 1)

  assert result1 == n_iter * n_epoches
  assert result2 == 0
  assert np.allclose(aux, np.arange(n_iter * n_epoches).reshape(n_epoches, n_iter))
  assert np.allclose(val1, np.zeros(n_epoches))
  assert np.allclose(val2, 100 * n_iter * np.arange(1, n_epoches + 1))
  assert np.allclose(val3, 200 * n_iter * np.arange(1, n_epoches + 1))

def test_batched():
  from tqdm import tqdm

  rng = jax.random.PRNGKey(112224333)
  rng, key_x, key_y, key_z = jax.random.split(rng, num=4)

  size = 1024
  batch = 127

  dataset = {
    'x': jax.random.normal(key_x, shape=(size, 3, 4)),
    'a': (
      jax.random.normal(key_y, shape=(size, )),
      jax.random.normal(key_z, shape=(size, 1, 1, 1, 7)),
    )
  }

  indx = np.zeros(shape=(3, size // batch), dtype=np.int32)

  for i, j, x in crayopt.train.batched(rng, dataset, epochs=3, batch=127, axis=0, progress=tqdm):
    indx[i, j] = 1
    assert x['x'].shape == (batch, *dataset['x'].shape[1:])
    assert x['a'][0].shape == (batch, *dataset['a'][0].shape[1:])
    assert x['a'][1].shape == (batch, *dataset['a'][1].shape[1:])

  assert np.all(indx == 1)



