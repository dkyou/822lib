#!/usr/bin/python
# coding:utf-8
# rr_IK.py
# Inverse kinematics IK
# The simplified single leg of mini pupper can be regarded as an RR robot arm on the same plane, visualize the robot arm, and calculate the rotation axis angle from the given end position
import matplotlib.pyplot as plt # import matplotlib
import numpy as np # import numpy
from math import degrees, sin, cos


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
    # print(cos2)
    sin2_1 = np. sqrt(1 - cos2 ** 2)
    sin2_2 = -sin2_1
    # print(sin2_1)
    # print("sin2 has two values, they are sin2_1=%f, sin2_2=%f" % (sin2_1, sin2_2)) # If you consider the joint situation, you can only take a positive value
    theta2_1 = np.arctan2(sin2_1, cos2)
    theta2_2 = np.arctan2(sin2_2, cos2)
    phi_1 = np.arctan2(l2 * sin2_1, l1 + l2 * cos2)
    phi_2 = np.arctan2(l2 * sin2_2, l1 + l2 * cos2)
    theta1_1 = np.arctan2(y, x) - phi_1
    theta1_2 = np.arctan2(y, x) - phi_2
    # print(degrees(theta1_1), degrees(theta1_2), degrees(theta2_1), degrees(theta2_2))
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


def annotate_angle(x0, y0, rad1, rad2, name, inverse=False):
    """
    draw angles for two lines
    :param x0: x coordinate of the center of the circle
    :param y0: x coordinate of the center of the circle
    :param rad1: starting angle
    :param rad2: end angle
    :param name: role name
    :param inverse: used to solve the overlapping problem of point 1
    :return: None
    """
    theta = np.linspace(rad1, rad2, 100)  # 0~rad
    r = 0.2  # circle radius
    x1 = r * np.cos(theta) + x0
    y1 = r * np.sin(theta) + y0
    plt.plot(x1, y1, color='red')
    plt.scatter(x0, y0, color='blue')
    degree = degrees((rad2 - rad1))
    if inverse:
        plt.annotate("%s=%.1f°" % (name, degree), [x0, y0], [x0 - r / 1.5, y0 - r / 1.5])
    else:
        plt.annotate("%s=%.1f°" % (name, degree), [x0, y0], [x0 + r / 1.5, y0 + r / 1.5])


# Joint information
# Arm length: 5 cm Arm length: 7.5 cm
link_length = [5, 7.5]  # in cm
# input end position
position_pre = input("Please enter the x-coordinate and y-coordinate of the end, separated by spaces:")
position = [float(n) for n in position_pre. split()]
print(position)

# Compute and preprocess plot data
joints_angles = position_2_theta(position[0], position[1], link_length[0], link_length[1])
# print(joints_angles)
figure1 = preprocess_drawing_data(joints_angles[0], joints_angles[2], link_length[0], link_length[1])
figure2 = preprocess_drawing_data(joints_angles[1], joints_angles[3], link_length[0], link_length[1])
# print(figure1)
# print(figure2)

# drawing
fig, ax = plt.subplots()  # build image
plt. axis("equal")
ax. grid()
plt.plot(figure1[0], figure1[1], color='black', label='method 1')
plt.scatter(figure1[0], figure1[1], color='black')
plt.plot(figure2[0], figure2[1], color='red', label='method 2')
plt.scatter(figure2[0], figure2[1], color='blue')
ax.set(xlabel='X', ylabel='Y', title='mini pupper IK RR model')
plt. legend()
# Annotation
annotate_angle(figure1[0][0], figure1[1][0], 0, joints_angles[0], "theta1_1")
annotate_angle(figure1[0][1], figure1[1][1], joints_angles[0], joints_angles[2]+joints_angles[0], "theta2_1")
annotate_angle(figure2[0][0], figure2[1][0], 0, joints_angles[1], "theta1_2", inverse=True)
annotate_angle(figure2[0][1], figure2[1][1], joints_angles[1], joints_angles[3]+joints_angles[1], "theta2_2")
plt.annotate("P(%d, %d)" % (position[0], position[1]), [figure1[0][2], figure1[1][2]], [figure1[0][2] + 0.1, figure1[1][2] + 0.1])
plt.tight_layout()
plt. show()

