import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# Define the origin and axes of the initial coordinate system A
o_A = np.array([0, 0, 0])
x_A = np.array([1, 0, 0])
y_A = np.array([0, 1, 0])
z_A = np.array([0, 0, 1])

# Define the translation vector from A to B
translation_vector = np.array([3, 2, 1])

# Calculate the origin and axes of the coordinate system B
o_B = o_A + translation_vector
x_B = x_A  # The orientation of B is the same as A
y_B = y_A
z_B = z_A

# Prepare the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Plot coordinate system A
ax.plot([o_A[0], x_A[0]], [o_A[1], x_A[1]], [o_A[2], x_A[2]], 'r-', label='x_A')
ax.plot([o_A[0], y_A[0]], [o_A[1], y_A[1]], [o_A[2], y_A[2]], 'g-', label='y_A')
ax.plot([o_A[0], z_A[0]], [o_A[1], z_A[1]], [o_A[2], z_A[2]], 'b-', label='z_A')

# Plot coordinate system B
ax.plot([o_B[0], x_B[0] + o_B[0]], [o_B[1], x_B[1] + o_B[1]], [o_B[2], x_B[2] + o_B[2]], 'r--', label='x_B')
ax.plot([o_B[0], y_B[0] + o_B[0]], [o_B[1], y_B[1] + o_B[1]], [o_B[2], y_B[2] + o_B[2]], 'g--', label='y_B')
ax.plot([o_B[0], z_B[0] + o_B[0]], [o_B[1], z_B[1] + o_B[1]], [o_B[2], z_B[2] + o_B[2]], 'b--', label='z_B')

# Plot translation vector
ax.plot([o_A[0], o_B[0]], [o_A[1], o_B[1]], [o_A[2], o_B[2]], 'k-', label='Translation Vector')

# Set legend
ax.legend()

# Show the plot
plt.show()

