from typing import TypeVar, Union

import jax

__all__ = [
  'BlackBoxOptimizer', 'Parameters'
]

Parameters = TypeVar('Parameters')

class BlackBoxOptimizer(object):
  State: type

  def initial_state(self, parameters: Parameters) -> 'State':
    raise NotImplementedError()

  def propose(self, rng: jax.Array, state: 'State', batch: tuple[int, ...]=()) -> Parameters:
    raise NotImplementedError()

  def __call__(self, proposal: Parameters, values: jax.numpy.ndarray, state: 'State') -> tuple[Parameters, 'State']:
    raise NotImplementedError()