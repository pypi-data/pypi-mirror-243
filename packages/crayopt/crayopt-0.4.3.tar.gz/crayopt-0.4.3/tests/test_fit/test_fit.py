import os

import numpy as np

import jax
import jax.numpy as jnp

import matplotlib.pyplot as plt

import crayopt


def eval_fit(plot_root, seed, algorithms, generate, trials=32):
  rng = jax.random.PRNGKey(seed)

  r_scores = {
    name: np.ndarray(shape=(trials, ))
    for name in algorithms
  }

  rng, key_dim, key_N = jax.random.split(rng, num=3)

  ns = jax.random.randint(key_dim, minval=1, maxval=7, shape=(trials, ))
  Ns = jax.random.randint(key_N, minval=10 * ns, maxval=100 * ns, shape=(trials, ))
  print(Ns)

  for i in range(trials):
    n: int = ns[i]
    N: int = Ns[i]

    for name, (train, predict) in algorithms.items():
      rng, key_gen = jax.random.split(rng, num=2)

      mu, sigma, xs, ys, xs_test, ys_test, var_y, true_params = generate(key_gen, n, N)

      params = train(xs, ys, mu=mu, sigma=sigma)
      ps_test = predict(xs_test, *params)

      mse = jnp.mean(jnp.square(ps_test - ys_test))

      r_scores[name][i] = 1 - mse / var_y

  for name in algorithms:
    print(name)
    print(
      ', '.join([
        '%.2lf' % (x, )
        for x in np.quantile(r_scores[name], q=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
      ])
    )
    fig = plt.figure(figsize=(7, 21))
    axes = fig.subplots(3, 1)
    axes[0].set_title('r-score distribution')
    bins = np.linspace(0, 1, num=11)
    hs, _ = np.histogram(r_scores[name], bins=bins)
    outside = np.sum(r_scores[name] < 0)

    axes[0].bar(bins, np.concatenate([[outside], hs]), width=0.1)
    axes[0].set_xticks(bins, ['fail'] + ['%.1lf' % (x, ) for x in bins[1:]])
    axes[1].set_title('r-score vs n sample / ndim')
    axes[1].scatter(Ns / ns, r_scores[name])
    axes[2].set_title('r-score vs ndim')
    axes[2].scatter(ns, r_scores[name])

    fig.savefig(os.path.join(plot_root, f'{name}.png'))
    plt.close(fig)

def test_lin_fit(plot_root, seed):
  def gen(rng, n, N):
    key_mu, key_sigma, key_eps, key_test, key_b, key_w = jax.random.split(rng, num=6)
    mu = jax.random.normal(key_mu, shape=(n,))
    sigma = jax.random.exponential(key_sigma, shape=())

    eps = jax.random.normal(key_eps, shape=(N, n))
    eps_test = jax.random.normal(key_test, shape=(N, n))
    xs = eps * sigma + mu
    xs_test = eps_test * sigma + mu

    b = jax.random.normal(key_b, shape=())
    w = jax.random.normal(key_w, shape=(n,))
    ys = jnp.matmul(xs, w) + b
    ys_test = jnp.matmul(xs_test, w) + b

    var_y = jnp.sum(jnp.square(sigma * w))

    return mu, sigma, xs, ys, xs_test, ys_test, var_y, (w, b)

  return eval_fit(
    plot_root=plot_root,
    seed=seed,
    algorithms={
      'lstsq': (crayopt.utils.fit.lstsq_fit, crayopt.utils.fit.lin_predict),
      'quick': (crayopt.utils.fit.quick_lin_fit, crayopt.utils.fit.lin_predict),
    },
    generate=gen
  )

def test_quad_fit(plot_root, seed):
  def gen(rng, n, N):
    key_mu, key_sigma, key_eps, key_test, key_b, key_w_lin, key_w_sqr = jax.random.split(rng, num=7)
    mu = jax.random.normal(key_mu, shape=(n,))
    sigma = jax.random.exponential(key_sigma, shape=())

    eps = jax.random.normal(key_eps, shape=(N, n))
    eps_test = jax.random.normal(key_test, shape=(N, n))
    xs = eps * sigma + mu
    xs_test = eps_test * sigma + mu

    b = jax.random.normal(key_b, shape=())
    w_lin = jax.random.normal(key_w_lin, shape=(n,))
    w_sqr = jax.random.normal(key_w_sqr, shape=(n,))

    f = lambda x: jnp.matmul(jnp.square(x), w_sqr) + jnp.matmul(x, w_lin) + b

    ys = f(xs)
    ys_test = f(xs_test)

    var_y = jnp.var(ys_test)

    return mu, sigma, xs, ys, xs_test, ys_test, var_y, (w_sqr, w_lin, b)

  return eval_fit(
    plot_root=plot_root,
    seed=seed,
    algorithms={
      'lstsq': (crayopt.utils.fit.lstsq_quad_fit, crayopt.utils.fit.quad_predict),
      # 'quick': (crayopt.utils.fit.quick_lin_fit, crayopt.utils.fit.lin_predict),
    },
    generate=gen
  )