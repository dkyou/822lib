#!/usr/bin/python
# coding:utf-8
# rr_IK_circle.py
# Inverse kinematics IK
# The simplified single leg of mini pupper can be regarded as an RR-like robotic arm on the same plane, and the inverse kinematics of the quadruped robot can be visualized and circled
import matplotlib.pyplot as plt # import matplotlib
import numpy as np # import numpy
from math import degrees, radians, sin, cos
import matplotlib.animation as animation


# Geometry method: end point coordinates to joint angles
def position_2_theta(x, y, l1, l2):
    """
    Kinematics inverse solution Convert the input endpoint coordinates into corresponding joint angles
    :param x: point p coordinate x value
    :param y: point p coordinate y value
    :param l1: arm length
    :param l2: forearm length
    :return: joint angle 1 value 1 joint angle 1 value 2 joint angle 2 value 1 joint angle 2 value 1
    """
    cos2 = (x ** 2 + y ** 2 - l1 ** 2 - l2 ** 2) / (2 * l1 * l2)
    sin2_1 = np. sqrt(1 - cos2 ** 2)
    sin2_2 = -sin2_1
    theta2_1 = np.arctan2(sin2_1, cos2)
    theta2_2 = np.arctan2(sin2_2, cos2)
    phi_1 = np.arctan2(l2 * sin2_1, l1 + l2 * cos2)
    phi_2 = np.arctan2(l2 * sin2_2, l1 + l2 * cos2)
    theta1_1 = np.arctan2(y, x) - phi_1
    theta1_2 = np.arctan2(y, x) - phi_2
    return theta1_1, theta1_2, theta2_1, theta2_2


def preprocess_drawing_data(theta1, theta2, l1, l2):
    """
    Process angle data and convert it to a drawing format adapted to matplotlib
    :param theta1: angle data 1
    :param theta2: angle data 2
    :param l1: bar length 1
    :param l2: bar length 2
    :return: x-coordinate list and corresponding y-coordinate list of drawing data
    """
    xs = [0]
    ys = [0]
    # Calculate x1 y1 and x2 y2 respectively
    x1 = l1 * cos(theta1)
    y1 = l1 * sin(theta1)
    x2 = x1 + l2 * cos(theta1 + theta2)
    y2 = y1 + l2 * sin(theta1 + theta2)
    xs.append(x1)
    xs.append(x2)
    ys.append(y1)
    ys.append(y2)
    return xs, ys


def animate_plot(n):
    # Generate circular trajectory
    circle_point = [2.696152422706633, -7.330127018922193]  # The center of the circular motion
    position = [0, 0]
    history_position_x = [0]
    history_position_y = [0]
    circle_r = 2
    theta = n * np.pi / 100
    position[0] = circle_point[0] + circle_r * np.cos(theta)
    position[1] = circle_point[1] + circle_r * np.sin(theta)

    # Compute and preprocess plot data
    joints_angles = position_2_theta(position[0], position[1], link_length[0], link_length[1])
    figure1 = preprocess_drawing_data(joints_angles[0], joints_angles[2], link_length[0], link_length[1])

    # Trajectory tracking
    for i in range(0, (n % 200)+1):
        history_theta = ((n % 200) + 1 - i) * np.pi / 100
        history_position_x.append(circle_point[0] + circle_r * np.cos(history_theta))
        history_position_y.append(circle_point[1] + circle_r * np.sin(history_theta))

    # drawing
    p = plt.plot(figure1[0], figure1[1], 'o-', lw=2, color='black')
    p += plt.plot(history_position_x, history_position_y, '--', color='blue', lw=1)
    return p


# Joint information
# Arm length: 5 cm Arm length: 7.5 cm
link_length = [5, 7.5]  # in cm

# matplotlib visualization part
fig, ax = plt.subplots()  # build image
plt. axis("equal")
plt. grid()
ax.set(xlabel='X', ylabel='Y', title='mini pupper IK RR model Circle Plot')
ani = animation.FuncAnimation(fig, animate_plot, interval=10, blit=True)
plt. show()

