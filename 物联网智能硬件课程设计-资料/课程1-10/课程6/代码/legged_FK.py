import matplotlib.pyplot as plt
import numpy as np
from math import degrees, radians, sin, cos


def theta_to_position_rr(l1, l2, theta1, theta2):
    point_1 = [l1 * cos(radians(theta1)), l1 * sin(radians(theta1))]
    point_2 = [l1 * cos(radians(theta1)) + l2 * cos(radians(theta1 + theta2)),
               l1 * sin(radians(theta1)) + l2 * sin(radians(theta1 + theta2))]
    return point_1, point_2


def annotate_angle(x0, y0, rad1, rad2, name, inverse=False):
    theta = np.linspace(rad1, rad2, 100)
    r = 0.3
    x1 = r * np.cos(theta) + x0
    y1 = r * np.sin(theta) + y0
    plt.plot(x1, y1, color='red')
    plt.scatter(x0, y0, color='blue')
    degree = degrees(rad2 - rad1)
    if inverse:
        plt.annotate("%s=%.1f°" % (name, degree), [x0, y0], [x0 - r / 1.5, y0 - r / 1.5])
    else:
        plt.annotate("%s=%.1f°" % (name, degree), [x0, y0], [x0 + r / 1.5, y0 + r / 1.5])


# Link lengths and joint angles
l1, l2 = 5, 6
theta1, theta2 = -150, 90

# Calculate joint positions
point_1, point_2 = theta_to_position_rr(l1, l2, theta1, theta2)

# Create a new figure and axis
fig, ax = plt.subplots()

# Set up the coordinate system and grid
ax.set(xlabel='X', ylabel='Y', title='Four-legged Robot Leg RR Model')
ax.grid()
plt.axis("equal")

# Draw L1 and L2
plt.plot([0, point_1[0]], [0, point_1[1]], 'k-', linewidth=2, label='L1')
plt.plot([point_1[0], point_2[0]], [point_1[1], point_2[1]], 'r-', linewidth=2, label='L2')

# Draw joints and end effector
plt.scatter([0, point_1[0], point_2[0]], [0, point_1[1], point_2[1]], color='blue', zorder=3)

# Annotate joint angles
annotate_angle(0, 0, 0, radians(theta1), "theta1", inverse=True)
annotate_angle(point_1[0], point_1[1], radians(theta1), radians(theta1 + theta2), "theta2", inverse=True)

# Annotate end effector position
plt.annotate("P(%.1f, %.1f)" % (point_2[0], point_2[1]), point_2, [point_2[0] + 0.2, point_2[1] + 0.2])

plt.legend(loc=2)
plt.show()

