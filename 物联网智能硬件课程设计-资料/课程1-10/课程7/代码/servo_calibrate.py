#!/usr/bin/python
# coding:utf-8
# servo_calibrate.py
# By default, all servos return to zero, and then wait for the input angle

import RPi.GPIO as GPIO
import time


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


signal_ports = input(
    "Enter the signal port numbers of each servo, separated by spaces, press Enter if there is no input, the default signal port is: 32 33 35\nPlease enter:") or "32 33 35"
signal_ports = [int(n) for n in signal_ports. split()]
for i in range(0, len(signal_ports)):
    print("The port corresponding to steering gear %d is %d" %
          (i+1, signal_ports[i]))

GPIO.setmode(GPIO.BOARD)  # Initialize GPIO pin coding mode
servo = [0, 0, 0]
servo_SIG = signal_ports  # PWM signal port
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
print("Initialization back to zero is complete, wait for input after two seconds")
time. sleep(2)

# Specify the position for the servo
try:  # try and except are a fixed combination, used to capture whether the user presses ctrl+C to terminate the program during execution
    while 1:
        angles = input(
            "If you need to change the angle of the servo, please input the angle value of 0°-180° for different servos:\n")
        angles = [int(n) for n in angles. split()]

        for i in range(0, len(angles)):
            dc_trans = servo_map(
                angles[i], 0, 180, servo_width_min, servo_width_max)
            servo[i].ChangeDutyCycle(dc_trans)
            print("The servo %d has turned to %d°" % (i+1, angles[i]))
except KeyboardInterrupt:
    pass
for i in range(0, len(servo_SIG)):
    servo[i].stop()  # stop pwm
GPIO.cleanup()  # Clean up GPIO pins

