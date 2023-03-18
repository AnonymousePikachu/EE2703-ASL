import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Create the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the x, y, and z data
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)

# Create the surface plot
surf = ax.plot_surface(X, Y, Z)

# Define the update function
def update(frame):
    # Shift the plane up and down
    Z[:,:] = np.sin(frame/10)
    surf.set_array(Z.ravel())
    return surf,

# Create the animation
ani = FuncAnimation(fig, update, frames=1000, interval=50)

# Set the limits for the x, y, and z axes
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-1, 1)

# Show the plot
plt.show()
