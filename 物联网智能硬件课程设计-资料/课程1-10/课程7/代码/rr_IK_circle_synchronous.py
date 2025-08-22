#!/usr/bin/python
# coding:utf-8
# rr_IK_circle_synchronous.py
# Kinematics inverse solution to draw a circle, synchronize the image display of the control terminal and the hardware movement
import matplotlib.pyplot as plt  # import matplotlib
import numpy as np  # import numpy
from math import degrees, sin, cos
import matplotlib.animation as animation
import time
import RPi.GPIO as GPIO


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


def servo_map(before_value, before_range_min, before_range_max, after_range_min, after_range_max):
    """
    Function: Map a range of values to another range of values
    Parameters: a certain value in the original range, the minimum value in the original range, the maximum value in the original range, the minimum value in the transformed range, and the maximum value in the transformed range
    Return: the transformed range corresponds to a certain value
    """
    percent = (before_value - before_range_min) / \
        (before_range_max - before_range_min)
    after_value = after_range_min + percent * \
        (after_range_max - after_range_min)
    return after_value


def theta_to_servo_degree(theta, servo_number, relation_list, config_calibration_value=None):
    """
    Convert the angle of the rod to the angle of the steering gear
    :param theta: member angle in radians
    :param servo_number: servo number
    :param relation_list: Servo relationship mapping table
    :param config_calibration_value:
    :return: servo angle in angle system
    """
    if config_calibration_value is None:
        config_calibration_value = [0, 0, 0]
    theta = degrees(theta)
    servo_degree = 0
    if servo_number == 1:
        # print("servo1")
        servo_degree = 0  # here needs to be modified according to servo 1
    elif servo_number == 2:
        # print("servo2")
        servo_degree = theta + relation_list[1] + config_calibration_value[1]
    elif servo_number == 3:
        # print("servo3")
        servo_degree = theta + relation_list[2] + config_calibration_value[2]
    else:
        # print("ERROR: theta_to_servo_degree")
        servo_degree = 0
    return servo_degree


def servo_control(servo_number, degree):
    """
    Use the angle value to control the corresponding angle of the motor output
    :return:
    """
    dc_trans = servo_map(degree, 0, 180, servo_width_min, servo_width_max)
    servo[servo_number - 1].ChangeDutyCycle(dc_trans)
    print("Servo %d has turned to %f°" % (servo_number, degree))


def circle_point_generate(center_point, radius, frame):
    """
     Enter the center of the circle [x0, y0], the radius r, and the count c, and return the coordinates [x, y] of a single point on the circumference
    :param center_point: circle center [x0,y0]
    :param radius: radius
    :param frame: the number of sample points for segmentation
    :return: A list of two arrays composed of the coordinates [x,y] of a single point on the circumference
    """
    theta = np.linspace(0, 2 * np.pi, frame)
    xs = center_point[0] + radius * np.cos(theta)
    ys = center_point[1] + radius * np.sin(theta)
    return xs, ys


def preprocess_drawing_data(theta1, theta2, l1, l2):
    """
    Process angle data and convert it to a drawing format adapted to matplotlib
    :param theta1: angle data 1
    :param theta2: angle data 2
    :param l1: bar length 1
    :param l2: bar length 2
    :return: x-coordinate array and y-coordinate array of leg points
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


def animation_update(frame):
    """
    Update animation and sync to hardware motor
    Note: The matplotlib online animation lock frame is at 30fps, and the frame should not be higher than 30
    :param frame:
    :return:
    """
    # Hardware servo motion synchronization
    servo_control(1, servo_degree[0][frame])
    servo_control(2, servo_degree[1][frame])

    # Update circle drawing
    circle_artist.set_xdata(xs[0:frame])  # set x directly
    circle_artist.set_ydata(ys[0:frame])  # set y directly
    # update leg drawing
    leg_artist.set_xdata(leg_data_xs[frame])  # set x directly
    leg_artist.set_ydata(leg_data_ys[frame])  # set y directly
    return circle_artist, leg_artist


# Configuration and initialization
center_point = [1.767767, -8.838835]  # The center of the circular motion
radius = 2  # circle radius
frame = 60  # number of split samples
leg_data_xs = []  # data x of each point of leg
leg_data_ys = []  # Data y of each point of leg
position = [0, 0]  # The position passed to the servo
link_length = [5, 7.5]  # Length of the member in cm
config_degree_relation_list = [+0, +225, +0]
servo = [0, 0, 0]
servo_degree = [[], []]  # Servo data table
servo_SIG = [32, 33]  # PWM signal terminal
servo_VCC = [2, 4, 1]  # VCC terminal
servo_GND = [30, 34, 39]  # GND terminal
servo_freq = 50  # PWM frequency
servo_width_min = 2.5  # Minimum working pulse width
servo_width_max = 12.5  # maximum working pulse width
GPIO.setmode(GPIO.BOARD)  # Initialize GPIO pin coding mode
for i in range(0, len(servo_SIG)):
    GPIO.setup(servo_SIG[i], GPIO.OUT)
    servo[i] = GPIO.PWM(servo_SIG[i], servo_freq)
    servo[i].start(0)
    # Return to the center position of the servo
    servo[i].ChangeDutyCycle((servo_width_min + servo_width_max) / 2)


# circle trajectory generation
xs, ys = circle_point_generate(center_point, radius, frame)
# leg trajectory generation
for i in range(0, frame):
    position[0] = xs[i]
    position[1] = ys[i]
    # Get kinematics inverse solution value
    joints_angles = position_2_theta(
        position[0], position[1], link_length[0], link_length[1])
    # Convert the inverse solution value to the drawing data
    leg_data_pre = preprocess_drawing_data(
        joints_angles[0], joints_angles[2], link_length[0], link_length[1])
    leg_data_xs.append(leg_data_pre[0])
    leg_data_ys.append(leg_data_pre[1])
    # Rod angle to servo angle
    servo_degree[0].append(theta_to_servo_degree(
        joints_angles[0], 2, config_degree_relation_list))
    servo_degree[1].append(theta_to_servo_degree(
        joints_angles[2], 3, config_degree_relation_list))

print("Initialization is complete, wait for operation after 1 second")
time. sleep(1)
# matplotlib visualization part
fig, ax = plt.subplots(figsize=(6, 6))  # create image
plt. axis("equal")
plt. grid()
circle_artist = ax.plot(xs[0], ys[0], '--', lw=2, color='blue')[0]
leg_artist = ax.plot(
    leg_data_xs[0], leg_data_ys[0], 'o-', lw=2, color='black')[0]
ax.set(xlim=[-6, 7], ylim=[-12, 1], xlabel='X', ylabel='Y',
       title='mini pupper IK RR model Circle Plot')
# plt. tick_params(axis="both")
# set animation, interval unit is ms
ani = animation.FuncAnimation(
    fig=fig, func=animation_update, frames=frame, interval=1, blit=True)

plt. show()
plt.clf("all")
for i in range(0, len(servo_SIG)):
    servo[i].stop()  # stop pwm
GPIO.cleanup()  # Clean up GPIO pins
