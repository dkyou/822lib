#!/usr/bin/python
# coding:utf-8
#led_blink_GPIO.py
# Change the on and off state of the LED light connected to the GPIO of the Raspberry Pi periodically, and the continuous bright and dark flicker with a cycle of two seconds.

import RPi.GPIO as GPIO
import time

# GPIO initialization
LED = 33
period = 2
GPIO.setmode(GPIO.BOARD) # Initialize GPIO pin coding mode
GPIO.setup(LED, GPIO.OUT)
# If you need to ignore pin multiplexing warnings, please call GPIO.setwarnings(False)
# GPIO. setwarnings(False)
print('The preset is completed, it starts to flash, the port is %d, and the period is %d seconds.' % (LED, period))

while True:
     GPIO. output(LED, GPIO. HIGH)
     time. sleep(period/2)
     GPIO. output(LED, GPIO. LOW)
     time. sleep(period/2)

GPIO.cleanup()
