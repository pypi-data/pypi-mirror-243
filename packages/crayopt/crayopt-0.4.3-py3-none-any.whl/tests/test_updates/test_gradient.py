import os
import numpy as np

import jax
import jax.numpy as jnp

import matplotlib.pyplot as plt

import pytest

from crayopt import functions

def test_gradient(plot_root):
  from crayopt import gradient

  n_steps = 1024

  trajectories = dict()
  losses = dict()
  grids = dict()

  for func_name in functions.__all__:
    trajectories[func_name] = dict()
    losses[func_name] = dict()

    func: functions.TargetFunction = getattr(functions, func_name)
    x0 = jnp.array(func.initial_guess(), dtype=jnp.float32)

    @jax.jit
    def target(x):
      return func(x)

    grad = jax.jit(jax.grad(target, argnums=0))

    for method_name in gradient.__optimizers__:
      trajectories[func_name][method_name] = np.zeros(shape=(n_steps, len(x0)))
      losses[func_name][method_name] = np.zeros(shape=(n_steps, ))

      optimizer: gradient.GradientOptimizer = getattr(gradient, method_name)()
      state = optimizer.initial_state(x0)

      def step(x, s):
        x_, s_ = optimizer(x, grad(x), s)
        return target(x_), x_, s_

      x = x0
      for i in range(n_steps):
        t, x, state = step(x, state)
        losses[func_name][method_name][i] = float(t)
        trajectories[func_name][method_name][i] = np.array(x)


    if len(func.search_domain()) == 2:
      lower = jnp.array(func.initial_guess(), dtype=jnp.float32)
      upper = jnp.array(func.initial_guess(), dtype=jnp.float32)

      for method_name in trajectories[func_name]:
        lower = jnp.minimum(
          lower,
          jnp.min(trajectories[func_name][method_name], axis=0),
        )

        upper = jnp.maximum(
          upper,
          jnp.max(trajectories[func_name][method_name], axis=0),
        )

        delta = jnp.max(upper - lower)
        center = (lower + upper) / 2

        lower, upper = center - 0.5 * delta, center + 0.5 * delta

      xs, ys = (
        jnp.linspace(lower[i], upper[i], num=128)
        for i in range(2)
      )

      grid = jnp.stack(
        jnp.meshgrid(xs, ys, indexing='ij'),
        axis=-1
      )

      grids[func_name] = (
        xs, ys, grid, func(grid.reshape((-1, 2))).reshape(grid.shape[:2])
      )

    else:
      grids[func_name] = None

  plt.figure(figsize=(12, 6 * len(losses)))

  for i, func_name in enumerate(losses):
    plt.subplot(len(losses), 1, i + 1)
    plt.title(func_name)

    func = getattr(functions, func_name)

    for j, method_name in enumerate(losses[func_name]):
      plt.plot(
        losses[func_name][method_name],
        color=plt.cm.tab20(j),
        label=method_name if jnp.all(jnp.isfinite(losses[func_name][method_name])) else '%s (failed)' % (method_name, )
      )

    optimum = func(np.array(func.optimum()))
    plt.plot([0, n_steps - 1], [optimum, optimum], color='black', linestyle='--')
    plt.legend(loc='upper right')
    plt.yscale('log')

  plt.savefig(os.path.join(plot_root, 'losses.png'))
  plt.close()

  targets_2d = [
    func_name for func_name in functions.__all__
    if len(getattr(functions, func_name).initial_guess()) == 2
  ]

  plt.figure(figsize=(9, 9 * len(targets_2d)))

  for i, func_name in enumerate(targets_2d):
    plt.subplot(len(targets_2d), 1, i + 1)
    plt.title(func_name)

    xs, ys, grid, fs = grids[func_name]

    for j, method_name in enumerate(losses[func_name]):
      levels = jnp.quantile(fs, q=jnp.linspace(0, 1, num=22)[1:-1])
      plt.contour(grid[:, :, 0], grid[:, :, 1], fs, levels=levels, colors='black')
      plt.plot(
        trajectories[func_name][method_name][:, 0], trajectories[func_name][method_name][:, 1],
        color=plt.cm.tab20(j), label=method_name
      )

    plt.legend(loc='upper right')

  plt.savefig(os.path.join(plot_root, 'trajectories.png'))
  plt.close()


@pytest.mark.parametrize('func', [functions.rosenbrock_2d_log1p, ])
def test_performance(seed, plot_root, func: functions.TargetFunction):
  import scipy.optimize as sciopt
  from crayopt import gradient

  n_train = 32
  n_test = 1024
  n_steps = 1024

  key = jax.random.PRNGKey(seed)
  (x1_min, x1_max), (x2_min, x2_max) = func.search_domain()
  x_min, x_max = jnp.array([x1_min, x2_min], dtype=jnp.float32), jnp.array([x1_max, x2_max], dtype=jnp.float32)
  key_train, key_test, key = jax.random.split(key, 3)
  u_train = jax.random.uniform(key_train, shape=(n_train, 2), dtype=jnp.float32)
  u_test = jax.random.uniform(key_test, shape=(n_test, 2), dtype=jnp.float32)

  initial_guesses = u_train * (x_max - x_min)[None, :] + x_min[None, :]
  initial_guesses_test = u_test * (x_max - x_min)[None, :] + x_min[None, :]
  initial_fs = func(initial_guesses)

  solution = jnp.array(func.optimum(), dtype=jnp.float32)
  grad = jax.jit(jax.grad(func))

  def get_optimizer(method):
    @jax.jit
    def optimizer(x0, *args):
      opt = method(*args)
      state0 = opt.initial_state(x0)

      def step(carry, _):
        x, s = carry

        df = grad(x)
        x_, s_ = opt(x, df, s)

        return (x_, s_), x_

      _, xs = jax.lax.scan(
        step, init=(x0, state0), length=n_steps, xs=None
      )

      return xs

    return optimizer


  def get_target(optimizer, reparametrization):
    weights = np.exp(-np.arange(n_steps))[::-1]
    def target(params):
      reparams = reparametrization(params)

      xs = np.stack([
        optimizer(x0, *reparams)
        for x0 in initial_guesses
      ], axis=0)

      return np.mean(
        np.sqrt(np.sum(np.square(xs[:, -1, :] - solution[None, :])))
      )

    return target

  def sgd_reparam(params):
    log_lr, = params
    return (
      jax.nn.softplus(log_lr),
    )

  def adam_reparam(params):
    log_lr, logit_beta1, logit_beta2 = params
    return (
      jax.nn.softplus(log_lr),
      jax.nn.sigmoid(logit_beta1),
      jax.nn.sigmoid(logit_beta2),
    )

  methods = dict(
    sgd=(
      gradient.sgd, sgd_reparam,
      [-7, ],
      [[-7, 3]]
    ),
    adam=(
      gradient.adam, adam_reparam,
      [-7, 2, 4],
      [(-9, 3), (-7, 7), (-7, 7)]
    ),
  )

  optimizers = {
    name: get_optimizer(method)
    for name, (method, _, _, _) in methods.items()
  }

  targets = {
    name: get_target(optimizers[name], reparam)
    for name, (_, reparam, _, _) in methods.items()
  }

  results = {
    name : sciopt.minimize(
      targets[name],
      x0=np.array(initial_params, dtype=np.float32),
      bounds=bounds,
      method='Powell'
    )
    for name, (_, _, initial_params, bounds) in methods.items()
  }

  print(results)

  for name in results:
    assert results[name].success, '%s\n%s' % (name, str(results[name]))

  trajectories = {
    name: [
      optimizers[name](x0, *reparam(results[name].x))
      for x0 in initial_guesses_test
    ]
    for name, (_, reparam, initial_params, _) in methods.items()
  }

  values = {
    name: np.stack([
      func(xs) / func(x0) for x0, xs in zip(initial_guesses_test, trajectories[name])
    ], axis=0)
    for name in methods
  }

  lower, upper = solution, solution

  for name in trajectories:
    for xs in trajectories[name]:
      lower = jnp.minimum(lower, jnp.min(xs, axis=0))
      upper = jnp.maximum(upper, jnp.max(xs, axis=0))

  center = (lower + upper) / 2
  delta = (upper - lower) / 2
  lower, upper = center - 1.05 * delta, center + 1.05 * delta

  xs, ys = (
    jnp.linspace(lower[i], upper[i], num=128)
    for i in range(2)
  )

  grid_xs = jnp.stack(
    jnp.meshgrid(xs, ys, indexing='ij'),
    axis=-1
  )

  grid_fs = func(grid_xs.reshape((-1, 2))).reshape(grid_xs.shape[:-1])

  quantiles = (0.1, 0.2, 0.3, 0.4)

  plt.figure(figsize=(12, 24))
  plt.subplot(2, 1, 1)
  for i, name in enumerate(values):
    _, reparam, _, _ = methods[name]
    label = '%s(%s)' % (
      name,
      ', '.join(['%.3e' % (x,) for x in reparam(results[name].x)])
    )
    for j, q in enumerate(quantiles):
      plt.fill_between(
        np.arange(n_steps),
        np.quantile(values[name], axis=0, q=q),
        np.quantile(values[name], axis=0, q=1 - q),
        color=plt.cm.tab20(i),
        alpha=0.5 / len(quantiles)
      )
    plt.plot(np.arange(n_steps), np.median(values[name], axis=0), label=label, color=plt.cm.tab20(i))

  plt.yscale('log')
  plt.legend(loc='upper right')

  plt.subplot(2, 1, 2)
  plt.contour(
    grid_xs[:, :, 0], grid_xs[:, :, 1], grid_fs,
    colors='black',
    levels=np.quantile(grid_fs, q=np.linspace(0, 1, num=12)[1:-1])
  )
  plt.scatter([solution[0]], [solution[1]], marker='*')

  for i, name in enumerate(trajectories):
    for j, xs in enumerate(trajectories[name]):
      plt.plot(xs[:, 0], xs[:, 1], label=name if j == 0 else None, color=plt.cm.tab20(i), alpha=0.25)
  plt.legend(loc='lower left')

  plt.savefig(os.path.join(plot_root, 'losses.png'))
  plt.close()