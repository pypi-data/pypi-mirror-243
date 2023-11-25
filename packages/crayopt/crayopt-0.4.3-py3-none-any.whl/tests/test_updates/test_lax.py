from collections import namedtuple

import jax
import jax.numpy as jnp
import crayopt

def test_lax(seed, ):
  Point = namedtuple('Point', ['A', 'y', 'z'])
  rng = jax.random.PRNGKey(seed)

  def f(p: Point):
    return jnp.sum(p.A, axis=(-2, -1)) + p.y + p.z

  p0 = Point(
    A=jnp.array([[1.0, 0.5], [0.5, 1]], dtype=jnp.float32),
    y=jnp.array(1.0, dtype=jnp.float32),
    z=jnp.array(1.0, dtype=jnp.float32),
  )

  optimizer = crayopt.LinLAX(sigma=1e-2, gradient=crayopt.sgd(learning_rate=1e-3))
  state = optimizer.initial_state(p0)

  proposal = optimizer.propose(rng, state, batch=(1024, ))
  fs = f(proposal)

  eps = jax.tree_util.tree_map(lambda x, m: (x - m) / optimizer.sigma, proposal, state.mu)
  _, grad_lax = optimizer.value_and_grad_c(eps, state.mu, optimizer.fit(proposal, fs, state.mu))
  grad = jax.grad(f)(state.mu)

  for name, gl, g in zip(Point._fields, grad_lax, grad):
    print(name)
    print(gl)
    print(g)

  # estimate, state_updated = optimizer(proposal, fs, state)
  #
  # print(estimate)
  # print(state_updated)