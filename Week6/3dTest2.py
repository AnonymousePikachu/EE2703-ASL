import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Create the figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define the x, y, and z data
t = np.linspace(0, 10*np.pi, 1000)
x = np.cos(t)
y = np.sin(t)
z = t

# Create the line plot
line, = ax.plot(x, y, z)

# Define the update function
def update(frame):
    # Rotate the plot by changing the view angle
    ax.view_init(elev=10, azim=frame/2)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=360, interval=50)

# Set the limits for the x, y, and z axes
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(0, 10*np.pi)

# Show the plot
plt.show()
