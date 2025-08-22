#!/usr/bin/python
#coding:utf-8
#led_blink.py
# Make the state of the Raspberry Pi status indicator light change periodically, with a period of one second of continuous light and dark flashing.

from time import sleep
status_led = open('/sys/class/leds/led1/brightness', 'wb', 0)
# mini pupper disables the indicator light after it is turned on by default. If led1 cannot flash, you can change it to led0 here
# If you want to enable the LED, please modify /boot/firmware/config.txt
# The specific method of modifying config.txt can be found in the example 1 part of the advanced reference document of the course
while True:
     status_led.write(b'0') # Turn on
     sleep(0.5)
     status_led.write(b'1') # Turn off
     sleep(0.5)
