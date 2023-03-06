# Magic command below to enable interactivity in the JupyterLab interface
#%matplotlib ipympl
# Some basic imports that are useful
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'r')
def init():
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    return ln, 
def update(frame):
    xdata, ydata = morph(xs, ys, xc, yc, frame)
    ln.set_data(xdata, ydata)
    return ln,
def circle(t):
    return np.cos(t), np.sin(t)
def square(t):
    """Return x and y coordinates for a square in +/-0.5."""
    n4 = int(len(t) / 4)
    ts = np.linspace(-0.5, +0.5, n4)
    xs = np.concatenate([ts, 0.5*np.ones(n4), ts[::-1], -0.5*np.ones(n4)])
    ys = np.concatenate([xs[n4:], xs[:n4]])
    return xs, ys
def morph(x1, y1, x2, y2, alpha):
    xm = alpha * x1 + (1-alpha) * x2
    ym = alpha * y1 + (1-alpha) * y2
    return xm, ym
t = np.linspace(3*np.pi/4, -5*np.pi/4, 200)
if len(t) % 4 != 0:
    raise BaseException("Number of points should be multiple of 4...")
xc, yc = circle(t)
xs, ys = square(t)
# print(f"Square: {np.shape(xs)}")
ani = FuncAnimation(fig, update, frames=np.linspace(0, 1, 128),
init_func=init, blit=True, interval=10, repeat=True)
plt.show()
