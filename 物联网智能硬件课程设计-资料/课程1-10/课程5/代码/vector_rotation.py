#!/usr/bin/python
# coding:utf-8
# vector_rotation.py
# Rotate a specified vector in the reference coordinate system by a specified angle around the x, y, and z axes, and draw the original vector and the rotated vector in sequence in red, orange, green, and blue
import matplotlib.pyplot as plt
import numpy as np


def rotate_X(x, y, z, alpha):
    alpha_rad = np.radians(alpha)
    x_r = x
    y_r = np.cos(alpha_rad) * y - np.sin(alpha_rad) * z
    z_r = np.sin(alpha_rad) * y + np.cos(alpha_rad) * z
    return x_r, y_r, z_r


def rotate_Y(x, y, z, beta):
    beta_rad = np.radians(beta)
    x_r = np.cos(beta_rad) * x + np.sin(beta_rad) * z
    y_r = y
    z_r = -np.sin(beta_rad) * x + np.cos(beta_rad) * z
    return x_r, y_r, z_r


def rotate_Z(x, y, z, gamma):
    gamma_rad = np.radians(gamma)
    x_r = np.cos(gamma_rad) * x - np.sin(gamma_rad) * y
    y_r = np.sin(gamma_rad) * x + np.cos(gamma_rad) * y
    z_r = z
    return x_r, y_r, z_r


def draw_vector(ax, origin, vector, color):
    ax.quiver(origin[0], origin[1], origin[2],
              vector[0], vector[1], vector[2],
              arrow_length_ratio=0.1, color=color)


def draw_axes(ax, origin, length):
    x_axis = [length, 0, 0]
    y_axis = [0, length, 0]
    z_axis = [0, 0, length]
    draw_vector(ax, origin, x_axis, 'black')
    draw_vector(ax, origin, y_axis, 'black')
    draw_vector(ax, origin, z_axis, 'black')


def main():
    # Initialize plot
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set(xlim3d=(0, 5), xlabel='X')
    ax.set(ylim3d=(0, 5), ylabel='Y')
    ax.set(zlim3d=(0, 5), zlabel='Z')

    # Initialize variables
    origin = [0, 0, 0]
    length = 4
    draw_axes(ax, origin, length)

    vector_input = input("Please enter the x, y, z components of the vector, separated by spaces:")
    vector = [float(n) for n in vector_input. split()]
    rotation_input = input("Please enter the angle of rotation of the vector around the x, y, z axis (in degrees):")
    rotations = [float(n) for n in rotation_input.split()]

    draw_vector(ax, origin, vector, 'red')
    vector_rotated_x = rotate_X(*vector, rotations[0])
    draw_vector(ax, origin, vector_rotated_x, 'orange')
    vector_rotated_xy = rotate_Y(*vector_rotated_x, rotations[1])
    draw_vector(ax, origin, vector_rotated_xy, 'green')
    vector_rotated_xyz = rotate_Z(*vector_rotated_xy, rotations[2])
    draw_vector(ax, origin, vector_rotated_xyz, 'blue')

    plt.show()


if __name__ == "__main__":
    main()


