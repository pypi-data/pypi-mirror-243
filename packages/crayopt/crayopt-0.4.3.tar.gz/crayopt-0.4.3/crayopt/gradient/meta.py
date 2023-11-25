from typing import TypeVar

__all__ = [
  'GradientOptimizer',

  'Parameters'
]

Parameters = TypeVar('Parameters')


class GradientOptimizer(object):
  State: type

  def initial_state(self, parameters: Parameters) -> 'State':
    raise NotImplementedError()

  def __call__(self, parameters: Parameters, gradient: Parameters, state: 'State') -> tuple[Parameters, 'State']:
    raise NotImplementedError()