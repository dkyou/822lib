#!/usr/bin/python
# coding:utf-8
# rr_FK.py
# The simplified single leg of mini pupper can be regarded as an RR robot arm on the same plane, visualize the robot arm, and calculate the position of the end point from a given angle
import matplotlib.pyplot as plt  # import matplotlib
import numpy as np  # import numpy
from math import degrees, radians, sin, cos


# Geometry method: joint angle to endpoint coordinates
def theta_2_position_rr(l1, l2, theta1, theta2):
    """
    Kinematics positive solution Convert the input joint angle into the corresponding end point coordinates
    :param l1: arm length
    :param l2: forearm length
    :param theta1: arm joint angle
    :param theta2: forearm joint angle
    :return: endpoint 1 coordinates endpoint 2 coordinates
    """
    point_1 = [l1*cos(radians(theta1)), l1*sin(radians(theta1))]
    point_2 = [l1*cos(radians(theta1))+l2*cos(radians(theta1+theta2)),
               l1*sin(radians(theta1))+l2*sin(radians(theta1+theta2))]
    print(point_1)
    print(point_2)
    return point_1, point_2


def preprocess_drawing_data(points):
    """
    Process point coordinate data into a drawing format adapted to matplotlib
    :param points: point data
    :return: x-coordinate list and corresponding y-coordinate list of drawing data
    """
    xs = [0]
    ys = [0]
    xs.append(points[0][0])
    xs.append(points[1][0])
    ys.append(points[0][1])
    ys.append(points[1][1])
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
    r = 0.3  # circle radius
    x1 = r * np.cos(theta) + x0
    y1 = r * np.sin(theta) + y0
    plt.plot(x1, y1, color='red')
    plt.scatter(x0, y0, color='blue')
    degree = degrees((rad2 - rad1))
    if inverse:
        plt.annotate("%s=%.1f°" % (name, degree), [
                     x0, y0], [x0 - r / 1.5, y0 - r / 1.5])
    else:
        plt.annotate("%s=%.1f°" % (name, degree), [
                     x0, y0], [x0 + r / 1.5, y0 + r / 1.5])


# Joint information
# Arm length: 5 cm Arm length: 6 cm
link_length = [5, 6]  # in cm

# Joint angle initialization
joints_angle_origin = [-150, 90]
joints_angle = [0, 0]
print("Initial state of joint angle theta1=%d°, theta2=%d°" %
      (joints_angle_origin[0], joints_angle_origin[1]))

# Input link parameters: each joint angle
for i in range(1, 3):
    joints_angle[i-1] = int(
        input("Please input the angle to be turned by the leg servo [%d]:" % i))
    print("The leg servo[{0}] will turn {1}°".format(i, joints_angle[i-1]))
    joints_angle[i-1] = joints_angle_origin[i-1]+joints_angle[i-1]


# Compute and preprocess plot data
points_origin = theta_2_position_rr(
    link_length[0], link_length[1], joints_angle_origin[0], joints_angle_origin[1])
points_after = theta_2_position_rr(
    link_length[0], link_length[1], joints_angle[0], joints_angle[1])
data_origin = preprocess_drawing_data(points_origin)
data_after = preprocess_drawing_data(points_after)

# drawing
fig, ax = plt.subplots()  # build image
plt.plot(data_origin[0], data_origin[1], color='black', label='original')
plt.scatter(data_origin[0], data_origin[1], color='black')
plt.plot(data_after[0], data_after[1], color='red', label='after')
plt.scatter(data_after[0], data_after[1], color='blue')
ax.set(xlabel='X', ylabel='Y', title='mini pupper FK RR model')
ax. grid()
plt. axis("equal")
plt. legend(loc=2)

# Annotation
annotate_angle(data_origin[0][0], data_origin[1][0],
               0, radians(joints_angle_origin[0]), "theta1_original", inverse=True)
annotate_angle(data_origin[0][1], data_origin[1][1], radians(joints_angle_origin[0]),
               radians(joints_angle_origin[0]+joints_angle_origin[1]), "theta2_original", inverse=True)
annotate_angle(data_after[0][0], data_after[1][0],
               0, radians(joints_angle[0]), "theta1_after")
annotate_angle(data_after[0][1], data_after[1][1], radians(joints_angle[0]),
               radians(joints_angle[0]+joints_angle[1]), "theta2_after")
plt. show()

