#!/usr/bin/python
#coding:utf-8
#	led_blink.py 
#	使树莓派状态指示灯的亮灭状态周期性地改变，发生周期为一秒的持续明暗闪烁。

from time import sleep
status_led = open('/sys/class/leds/led1/brightness', 'wb', 0)
#	mini pupper 默认禁用了开启后的指示灯，如led1无法闪烁，此处可改为led0
#	如果你希望启用指示灯，请修改/boot/firmware/config.txt
#	修改config.txt的具体方法可查看课程的进阶参考文档中实例1部分
while True:
    status_led.write(b'0')	#	Turn on
    sleep(0.5)
    status_led.write(b'1')	#	Turn off
    sleep(0.5)