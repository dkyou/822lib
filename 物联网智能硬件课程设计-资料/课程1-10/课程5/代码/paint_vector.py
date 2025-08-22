import matplotlib.pyplot as plt
import numpy as np
# Create a 3D coordinate system
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Plot the origin of the coordinate system
ax.scatter(0, 0, 0, color='black', marker='o')

# Define the vector and normalize it
vector = np.array([3, 3, 3])
vector_norm = vector / np.linalg.norm(vector)

# Plot the vector
origin = np.array([0, 0, 0])
ax.quiver(*origin, *(vector_norm * 5), color='red')

# Set the axis limits
lim_left = 0
lim_right = 6
ax.set_xlim(lim_left, lim_right)
ax.set_ylim(lim_left, lim_right)
ax.set_zlim(lim_left, lim_right)

# Show the plot
plt.show()

