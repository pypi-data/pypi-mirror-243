import pytest
import numpy as np

@pytest.mark.skip(reason='Not a core functionality.')
def test_viz():
  from crayopt import viz
  from crayopt import functions

  samples = np.random.normal(size=(128, 2), scale=1e-1)[None, :, :] + \
            np.cumsum(np.random.normal(size=(1024, 128, 2), scale=1e-2), axis=0)

  samples = np.concatenate([samples, samples[::-1]], axis=0)

  xs, ys, F = viz.eval_on_grid(functions.rosenbrock_2d_log1p, (-2, 2), (-2, 2))

  background = viz.get_background(xs, ys, F, optimal=(1, 1))

  video = viz.animate(
    'out.mp4', samples, (-2, 2), (-2, 2), background, frames_per_second=64,
  )

  import os
  os.remove(video)
