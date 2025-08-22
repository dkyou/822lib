#!/usr/bin/python
# coding:utf-8
# led_blink_GPIO.py
# 使树莓派GPIO外接的LED灯的亮灭状态周期性地改变，发生周期为两秒的持续明暗闪烁。

import RPi.GPIO as GPIO
import time

# GPIO初始化
LED = 33
period = 2
GPIO.setmode(GPIO.BOARD)  # 初始化GPIO引脚编码方式
GPIO.setup(LED, GPIO.OUT)
# 如果你需要忽视引脚复用警告，请调用GPIO.setwarnings(False)
# GPIO.setwarnings(False)
print('预设置完成，开始闪烁，端口为%d，周期为%d秒。' % (LED, period))

while True:
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(period/2)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(period/2)

GPIO.cleanup()