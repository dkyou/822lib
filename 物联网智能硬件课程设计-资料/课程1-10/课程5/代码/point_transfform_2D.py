import numpy as np
import matplotlib.pyplot as plt

# Define the initial point P1
x = 2
y = 2
P1 = np.array([x, y])

# Calculate the polar coordinates (r, alpha)
r = np.sqrt(x**2 + y**2)
alpha = np.arctan2(y, x)

# Define the rotation angle theta in radians
theta = np.radians(45)  # 45 degrees

# Calculate the rotated point P2 using the rotation formula
x_prime = r * np.cos(alpha + theta)
y_prime = r * np.sin(alpha + theta)
P2 = np.array([x_prime, y_prime])

# Prepare the plot
fig, ax = plt.subplots()

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Plot the initial point P1
ax.plot(P1[0], P1[1], 'ro', label='P1 (x, y)')

# Plot the rotated point P2
ax.plot(P2[0], P2[1], 'bo', label="P2 (x', y')")

# Plot the lines connecting the origin to P1 and P2
ax.plot([0, P1[0]], [0, P1[1]], 'r--')
ax.plot([0, P2[0]], [0, P2[1]], 'b--')

# Plot the rotation angle theta
arc = plt.Circle((0, 0), r/2, color='g', fill=False, linestyle='--', linewidth=1)
ax.add_patch(arc)
ax.annotate(r'$\theta$', (r/2 * 0.7, r/2 * 0.3), fontsize=12, color='g')

# Annotate the angle between the line connecting the origin to P1 and the positive X-axis
ax.annotate(r'$\alpha$', (r/4 * 0.7, r/4 * 0.3), fontsize=12, color='r')

# Annotate the angle between the line connecting the origin to P2 and the positive X-axis
ax.annotate(r'$\alpha + \theta$', (r/1.5, r/1.5), fontsize=12, color='b')

# Set axis limits
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

# Set equal aspect ratio
ax.set_aspect('equal', adjustable='box')

# Add grid and set the aspect ratio
ax.grid(True)
ax.set_aspect('equal', adjustable='box')

# Plot the coordinate system
ax.axhline(y=0, color='k', linewidth=1)
ax.axvline(x=0, color='k', linewidth=1)

# Set legend
ax.legend()

# Show the plot
plt.show()

