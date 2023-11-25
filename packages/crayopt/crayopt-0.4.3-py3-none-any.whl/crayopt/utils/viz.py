import numpy as np

__all__ = [
  'get_grid',
  'eval_on_grid',
  'get_background',
  'animate'
]

def get_grid(range_x, range_y, steps=128):
  (min_x, max_x), (min_y, max_y) = range_x, range_y

  xs = np.linspace(min_x, max_x, num=steps, dtype=np.float32)
  ys = np.linspace(min_y, max_y, num=steps, dtype=np.float32)

  X_grid, Y_grid = np.meshgrid(xs, ys)
  XY_grid = np.stack([X_grid.ravel(), Y_grid.ravel()], axis=1)
  return xs, ys, XY_grid

def eval_on_grid(f, range_x, range_y, steps=128):
  xs, ys, XY_grid = get_grid(range_x, range_y, steps=steps)
  values = f(XY_grid)

  return xs, ys, np.array(values).reshape((xs.shape[0], ys.shape[0]))

def get_background(xs, ys, F, optimal=None, levels=20, figsize=(9, 9)):
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=figsize)

  f_min, f_max = np.min(F), np.max(F)
  levels = np.linspace(f_min, f_max, num=levels + 2)[1:-1]

  plt.contour(xs, ys, F.T, levels=levels, colors='black', zorder=0)

  if optimal is not None:
    opt_x, opt_y = optimal
    plt.scatter(opt_x, opt_y, marker='*', s=200, color='red', zorder=2)

  plt.xlim([xs[0], xs[-1]])
  plt.ylim([ys[0], ys[-1]])

  plt.axis('off')
  fig.tight_layout(pad=0)

  fig.canvas.draw()

  data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
  data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

  plt.close(fig)

  return data

def to_pixels(coords, bbox, geometry):
  indx = (coords - bbox[None, 0, :]) / (bbox[None, 1, :] - bbox[None, 0, :]) * geometry[None]
  indx = indx.astype('int32')

  in_bounds = (indx >= 0) & (indx < geometry[None, :])
  in_bounds, = np.where(in_bounds[:, 0] & in_bounds[:, 1])

  return indx[in_bounds, :]

def interpolate(img, geometry, bbox):
  from scipy.interpolate import RectBivariateSpline
  xs = np.linspace(bbox[0, 0], bbox[1, 0], num=img.shape[0])
  ys = np.linspace(bbox[0, 1], bbox[1, 1], num=img.shape[1])

  spline = RectBivariateSpline(xs, ys, img, kx=2, ky=2)

  target_xs = np.linspace(bbox[0, 0], bbox[1, 0], num=geometry[0])
  target_ys = np.linspace(bbox[0, 1], bbox[1, 1], num=geometry[1])

  interpolated = spline(target_xs, target_ys, grid=True)
  interpolated = np.clip(interpolated, 0, 1, out=interpolated)
  return interpolated[:, ::-1].T

def point_cloud_stream(
  samples, range_x, range_y,
  background, overlay=None, alpha=0.25,
  trace_decay=0.9,
  progress=lambda x, **kwargs: x
):
  x_min, x_max = range_x
  y_min, y_max = range_y
  bbox = np.array([[x_min, y_min], [x_max, y_max]])

  ### height, width are w.r.t. graph's coordinate system
  height, width = background.shape[:2]
  geometry = np.array([width, height])

  traces = np.zeros(shape=background.shape[:-1], dtype=np.float32)
  frame = np.zeros_like(background)

  if overlay is None:
    import itertools
    overlay = itertools.repeat(None)

  total = samples.shape[0] if hasattr(samples, 'shape') else None

  for sample, over in progress(zip(samples, overlay), total=total):
    indx = to_pixels(sample, bbox, geometry)
    if trace_decay is not None:
      np.multiply(traces, trace_decay, out=traces)
    else:
      traces[:] = 0

    traces[height - indx[:, 1] - 1, indx[:, 0]] += 1
    np.minimum(traces, 1, out=traces)

    np.multiply(background[..., 0], (1 - traces), out=frame[..., 0], casting='unsafe')
    np.multiply(background[..., 1], (1 - traces), out=frame[..., 1], casting='unsafe')
    np.multiply(background[..., 2], (1 - traces), out=frame[..., 2], casting='unsafe')
    frame[..., 2] = np.minimum(255 * traces + background[..., 2], 255).astype(np.uint8)

    if over is not None:
      over = alpha * interpolate(over, geometry, bbox)
      np.multiply(frame[..., 0], (1 - over), out=frame[..., 0], casting='unsafe')
      np.multiply(frame[..., 1], (1 - over), out=frame[..., 1], casting='unsafe')
      np.multiply(frame[..., 2], (1 - over), out=frame[..., 2], casting='unsafe')
      frame[..., 0] = np.minimum(255 * over + frame[..., 0], 255).astype(np.uint8)

    yield frame.tobytes()

def animate(
  filename,
  samples, range_x, range_y,
  background,
  overlay=None, overlay_alpha=0.25,
  trace_decay=0.9,
  frames_per_second=32,
  progress=lambda x, **kwargs: x,
  vcodec='vp9', format='webm',
  crf=31
):
  """
  Creates an animation of a point cloud with an optional overlay field.

  Note, that the overlay is in the traditional coordinate system,
  e.g., `overlay[0, 0]` is rendered in the bottom left of the plot, while background is in 'computer graphics'
  coordinate system with `background[0, 0]` rendered in the upper left corner.


  :param filename: output file name;
  :param samples: an array of shape (n frames, n points, 2), points to display, displayed in blue;
  :param range_x: horizontal coordinate range;
  :param range_y: vertical coordinate range;
  :param background: an RGB array of shape (width, height, 3), a background image;
  :param overlay: an array of shape (n frames, W, H), displayed in red;
  :param overlay_alpha: transparency of the overlay;
  :param trace_decay: if a float, keeps previous points, but applies transparency decay each frame;
  :param frames_per_second: number of frames per second;
  :param progress: tqdm to display the progress;
  :param vcodec: video codec to use, for details see ffmpeg documentation, vp9 by default;
  :param format: container format for the output video, webm by default;
  :param crf: controls video quality, must be between 0 and 63, lower values correspond to better quality.
  """
  import ffmpeg

  assert 0 <= crf <= 63, 'crf must be in the range [0, 63]'

  width = background.shape[1]
  height = background.shape[0]

  ff = ffmpeg.input(
    'pipe:', format='rawvideo', pix_fmt='rgb24',
    s='{}x{}'.format(width, height),
    r='%d' % (frames_per_second, )
  ).output(
    filename,
    vcodec=vcodec,
    pix_fmt='yuv420p', f=format,
    loglevel='panic',
    crf=crf, video_bitrate=0
  ).overwrite_output().run_async(
    pipe_stdin=True, quiet=True
  )

  stream = point_cloud_stream(
    samples, range_x, range_y,
    background, overlay=overlay,
    alpha=overlay_alpha, trace_decay=trace_decay,
    progress=progress
  )

  for frame in stream:
    ff.stdin.write(frame)

  ff.stdin.close()
  ff.wait()

  if ff.stderr is not None:
    stderr = ff.stderr.read()
    if len(stderr) > 0:
      print(stderr)

  return filename

def animate_contour():
  pass







