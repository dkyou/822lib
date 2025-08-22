import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the origin and axes of the initial coordinate system
o1 = np.array([0, 0, 0])
x1 = np.array([1, 0, 0])
y1 = np.array([0, 1, 0])
z1 = np.array([0, 0, 1])

# Define the object position and attitude in the initial coordinate system
p = np.array([3, 3, 3])
R = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])

# define coordinate system transformation
T = np.eye(4)
T[:3, :3] = R
T[:3, 3] = p

# Calculate the position and attitude of the object in the transformed coordinate system
o2 = T[:3, 3]
x2 = T[:3, :3] @ x1
y2 = T[:3, :3] @ y1
z2 = T[:3, :3] @ z1

# Prepare to draw
fig = plt. figure()

# set title
fig.suptitle('Object in Different Coordinate Systems')

# Draw the initial coordinate system and objects
ax1 = fig.add_subplot(121, projection='3d')
lim_left = -3
lim_right = 5
ax1.set_xlim(lim_left, lim_right)
ax1.set_ylim(lim_left, lim_right)
ax1.set_zlim(lim_left, lim_right)
ax1. set_xlabel('X')
ax1. set_ylabel('Y')
ax1. set_zlabel('Z')
ax1.set_title('Initial Coordinate System')
ax1.plot([o1[0], x1[0]], [o1[1], x1[1]], [o1[2], x1[2]], 'r-', label='x1' )
ax1.plot([o1[0], y1[0]], [o1[1], y1[1]], [o1[2], y1[2]], 'g-', label='y1' )
ax1.plot([o1[0], z1[0]], [o1[1], z1[1]], [o1[2], z1[2]], 'b-', label='z1' )
ax1.plot([p[0]], [p[1]], [p[2]], 'ko', label='object')
ax1. legend()

# Draw the transformed coordinate system and objects
ax2 = fig.add_subplot(122, projection='3d')
ax2.set_xlim(lim_left, lim_right)
ax2.set_ylim(lim_left, lim_right)
ax2.set_zlim(lim_left, lim_right)
ax2. set_xlabel('X')
ax2. set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Transformed Coordinate System')
ax2.plot([o2[0], x2[0]], [o2[1], x2[1]], [o2[2], x2[2]], 'r-', label='x2' )
ax2.plot([o2[0], y2[0]], [o2[1], y2[1]], [o2[2], y2[2]], 'g-', label='y2' )
ax2.plot([o2[0], z2[0]], [o2[1], z2[1]], [o2[2], z2[2]], 'b-', label='z2' )
ax2. legend()

plt. show()
