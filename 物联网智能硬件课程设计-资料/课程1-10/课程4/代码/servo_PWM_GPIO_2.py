#!/usr/bin/python
# coding:utf-8
#servo_PWM_GPIO_2.py
# Enter an angle value, the servo will turn to the corresponding angle
try:
     import RPi.GPIO as GPIO
except RuntimeError:
     print("Error importing RPi.GPIO! This is probably because you need superuser privileges."
           "You can achieve this by using 'sudo' to run your script")
import time


def servo_map(before_value, before_range_min, before_range_max, after_range_min, after_range_max):
     """
     Function: Map a range of values to another range of values
     Parameters: a certain value in the original range, the minimum value in the original range, the maximum value in the original range, the minimum value in the transformed range, and the maximum value in the transformed range
     Return: the transformed range corresponds to a certain value
     """
     percent = (before_value - before_range_min) / (before_range_max - before_range_min)
     after_value = after_range_min + percent * (after_range_max - after_range_min)
     return after_value


GPIO.setmode(GPIO.BOARD) # Initialize GPIO pin coding mode
servo_SIG = 32
servo_VCC = 4
servo_GND = 6
servo_freq = 50
servo_time = 0.01
servo_width_min = 2.5
servo_width_max = 12.5
# servo_degree_div =servo_width_max - servo_width_min)/180
GPIO.setup(servo_SIG, GPIO.OUT)
# If you need to ignore pin multiplexing warnings, please call GPIO.setwarnings(False)
# GPIO. setwarnings(False)
servo = GPIO.PWM(servo_SIG, servo_freq) # signal pin=servo_SIG frequency=servo_freq in HZ
servo.start(0)
servo.ChangeDutyCycle((servo_width_min+servo_width_max)/2) # Return to the center position of the servo
print('The preset is completed, wait for input after two seconds')
time. sleep(2)
# Specify the position for the servo
try: # try and except are a fixed combination, used to capture whether the user presses ctrl+C to terminate the program during execution
     while 1:
         position = input("Please enter the angle value of 0°-180°:\n")
         if position.isdigit()==1:
             dc = int(position)
             if (dc>=0) and (dc<=180):
                 dc_trans=servo_map(dc, 0, 180,servo_width_min,servo_width_max)
                 servo. ChangeDutyCycle(dc_trans)
                 print("Rotated to %d°"%dc)
             else:
                 print("Error Input: Exceeded Range")
         else:
             print("Error Input: Not Int Input")
except KeyboardInterrupt:
     pass

servo.stop() # stop pwm
GPIO.cleanup() # Clean up GPIO pins
