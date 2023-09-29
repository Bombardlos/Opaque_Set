import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Create a 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
pi = np.pi

# Create a meshgrid of points on the surface of the unit sphere
theta = np.linspace(0, 2 * pi, 100)
phi = np.linspace(0, pi, 100)
theta, phi = np.meshgrid(theta, phi)
r = 1  # Radius of the unit sphere
x = r * np.sin(phi) * np.cos(theta)
y = r * np.sin(phi) * np.sin(theta)
z = r * np.cos(phi)

# Create a 3D surface plot of the unit sphere
ax.plot_surface(x, y, z, color='gray', alpha=0.4)

# Create one half of the horizontal ring at a specific radius around the unit sphere
horizontal_ring_radius = np.sqrt(2)  # Radius of the horizontal ring
horizontal_ring_theta = np.linspace(0, pi, 100)  # One half of the circle
horizontal_ring_x = horizontal_ring_radius * np.cos(horizontal_ring_theta)
horizontal_ring_y = horizontal_ring_radius * np.sin(horizontal_ring_theta)
horizontal_ring_z = np.zeros_like(horizontal_ring_theta)  # Set z-coordinates to zero

# Plot the half-horizontal ring as a line
ax.plot(horizontal_ring_x, horizontal_ring_y, horizontal_ring_z, color='k')

# Create one half of the vertical ring at a specific radius around the unit sphere
vertical_ring_radius = np.sqrt(2)  # Radius of the vertical ring
vertical_ring_theta = np.linspace(pi/2, 3*pi/2, 100)  # One half of the circle
vertical_ring_x = np.zeros_like(vertical_ring_theta)  # Set x-coordinates to zero
vertical_ring_y = vertical_ring_radius * np.cos(vertical_ring_theta)
vertical_ring_z = vertical_ring_radius * np.sin(vertical_ring_theta)

# Plot the half-vertical ring as a line
ax.plot(vertical_ring_x, vertical_ring_y, vertical_ring_z, color='k')

# Set the aspect ratio to be equal
ax.set_aspect('equal')
#ax.set_xticks([])
#ax.set_yticks([])
#ax.set_zticks([])
ax.grid(color='black', alpha=0.1)

# Show the 3D plot
plt.show()
