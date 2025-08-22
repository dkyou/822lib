#!/usr/bin/python
# coding:utf-8
#led_breathe.py
# Raspberry Pi GPIO controls the breathing of the external LED light, and the cycle is 4 seconds.
import time
import RPi.GPIO as GPIO

# GPIO initialization
LED = 33 # Raspberry Pi PWM port connected to the external LED light, can be adjusted as needed
GND = 34 # port for ground
period = 4 # breath period
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
p = GPIO.PWM(LED, 50) # pin=LED frequency=50Hz
p.start(0)
print("PWM control breathing light starts, the port number is %d, and the period is %d seconds." % (LED, period))
try: # try and except are a fixed combination, used to capture whether the user presses ctrl+C to terminate the program during execution
     while 1:
         for dc in range(0, 101, 1):
             p. ChangeDutyCycle(dc)
             time. sleep(period / 200)
         for dc in range(100, -1, -1):
             p. ChangeDutyCycle(dc)
             time. sleep(period / 200)
except KeyboardInterrupt:
     pass
p. stop()
GPIO.cleanup()
