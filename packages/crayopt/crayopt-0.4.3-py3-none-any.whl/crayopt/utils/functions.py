import numpy as np
import jax.numpy as jnp

__all__ = [
  'quad_sqr',
  
  'rosenbrock_2d',
  'rosenbrock_2d_log1p',
  'rastrigin_2d',
  'beale',
  'beale_log1p',
]

class TargetFunction(object):
  def __init__(self, f, search_domain, optimum, initial_guess, name=None):
    self._f = f

    self._search_domain = search_domain
    self._optimum = optimum
    self._initial_guess = initial_guess
    self._name = name if name is not None else f.__name__

  def __call__(self, *args, **kwargs):
    return self._f(*args, **kwargs)

  def name(self):
    return self._name

  def search_domain(self):
    return self._search_domain

  def optimum(self):
    return self._optimum

  def initial_guess(self):
    return self._initial_guess

def target_function(search_domain, optimum, initial_guess, name=None):
  def wrapper(f):
    return TargetFunction(
      f=f,
      search_domain=search_domain,
      optimum=optimum,
      initial_guess=initial_guess,
      name=name
    )

  return wrapper

@target_function(search_domain=[(-0.5, -0.5), (0.5, 0.5)], optimum=(0, 0), initial_guess=(0.25, 0.25))
def quad_sqr(x):
  x_sqr = jnp.square(x)
  x_quad = jnp.square(x_sqr)

  return jnp.sum(x_sqr - x_quad, axis=-1)

@target_function(search_domain=[(-1, 2), (-1, 2)], optimum=(1, 1), initial_guess=(0, 1))
def rosenbrock_2d(x):
  return (1 - x[..., 0]) ** 2 + 100 * (x[..., 1] - x[..., 0] ** 2) ** 2

@target_function(search_domain=[(-1, 2), (-1, 2)], optimum=(1, 1), initial_guess=(0, 1))
def rosenbrock_2d_log1p(x):
  return jnp.log1p(
    (1 - x[..., 0]) ** 2 + 100 * (x[..., 1] - x[..., 0] ** 2) ** 2
  )

@target_function(search_domain=[(-1, 1), (-1, 1)], optimum=(0, 0), initial_guess=(0.45, 0.45))
def rastrigin_2d(x):
  return 20 + jnp.sum(
    jnp.square(x) - 10 * jnp.cos(2 * np.pi * x),
    axis=-1
  )

@target_function(search_domain=[(-4.5, 4.5), (-4.5, 4.5)], optimum=(3, 0.5), initial_guess=(0, 0))
def beale(x):
  x, y = x[..., 0], x[..., 1]
  return jnp.square(1.5 - x + x * y) + jnp.square(2.25 - x + x * jnp.square(y)) + jnp.square(2.625 - x + x * y ** 3)

@target_function(search_domain=[(-4.5, 4.5), (-4.5, 4.5)], optimum=(3, 0.5), initial_guess=(0, 0))
def beale_log1p(X):
  return jnp.log1p(beale(X))