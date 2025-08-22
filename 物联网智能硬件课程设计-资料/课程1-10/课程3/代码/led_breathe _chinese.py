#!/usr/bin/python
# coding:utf-8
# led_breathe.py
# 树莓派GPIO控制外部LED灯呼吸，周期为4秒。
import time
import RPi.GPIO as GPIO

# GPIO初始化
LED = 33    # 外部led灯连接的树莓派PWM端口，可根据需要调整
GND = 34    # 接地的端口
period = 4  # 呼吸周期
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
p = GPIO.PWM(LED, 50)  # 引脚=LED 频率=50Hz
p.start(0)
print("PWM控制呼吸灯开始，端口号为%d，周期为%d秒。" % (LED, period))
try:    # try和except为固定搭配，用于捕捉执行过程中，用户是否按下ctrl+C终止程序
    while 1:
        for dc in range(0, 101, 1):
            p.ChangeDutyCycle(dc)
            time.sleep(period / 200)
        for dc in range(100, -1, -1):
            p.ChangeDutyCycle(dc)
            time.sleep(period / 200)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()