from typing import Union, Optional

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

__all__ = [
  'losses'
]

def losses(
  loss_dict: Union[np.ndarray, dict[str, np.ndarray]],
  axes: Optional[plt.Axes]=None, figsize=(9, 6), cmap=plt.cm.tab10,
  quantiles: tuple[float, ...]=(0.1, 0.2, 0.3, 0.4, 0.5)
):

  if axes is None:
    fig = plt.figure(figsize=figsize)
    axes: plt.Axes = fig.subplots(1, 1)

  if not isinstance(loss_dict, dict):
    loss_dict = {None: loss_dict}

  for i, (name, ls) in enumerate(loss_dict.items()):
    xs = np.arange(ls.shape[0])

    if ls.ndim == 1:
      axes.plot(xs, ls, label=name, color=cmap(i))

    elif ls.ndim == 2:
      for j, q in enumerate(quantiles):
        if q == 0.5:
          median = np.median(ls, axis=1)
          axes.plot(xs, median, label=name, color=cmap(i))
        else:
          lower, upper = np.quantile(ls, axis=1, q=(q, 1 - q))
          axes.fill_between(xs, lower, upper, color=cmap(i), alpha=1 / len(quantiles))

  if len(loss_dict) > 1:
    axes.legend(loc='upper right')
  elif None in loss_dict or len(loss_dict) == 0:
    pass
  else:
    axes.legend(loc='upper right')

  return axes