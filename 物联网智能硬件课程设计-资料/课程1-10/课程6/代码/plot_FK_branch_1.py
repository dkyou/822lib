#!/usr/bin/python
# coding:utf-8
# rr_FK.py
# mini pupper的简化单腿，可视作同一平面的RR类机械臂，可视化该机械臂，由给定角度计算末端点位置
import matplotlib.pyplot as plt  # 引入matplotlib
import numpy as np  # 引入numpy
from math import degrees, radians, sin, cos


# 几何法：关节角转端点坐标
def theta_2_position_rr(l1, l2, theta1, theta2):
    """
    运动学正解 将输入的关节角转化为对应的端点坐标
    :param l1: 大臂长
    :param l2: 小臂长
    :param theta1: 大臂关节角
    :param theta2: 小臂关节角
    :return: 端点1坐标 端点2坐标
    """
    point_1 = [l1 * cos(radians(theta1)), l1 * sin(radians(theta1))]
    point_2 = [l1 * cos(radians(theta1)) + l2 * cos(radians(theta1 + theta2)),
               l1 * sin(radians(theta1)) + l2 * sin(radians(theta1 + theta2))]
    return point_1, point_2


def preprocess_drawing_data(points):
    """
    处理点坐标数据转化为matplotlib适应的绘图格式
    :param points: 点数据
    :return: 绘图数据x坐标list和对应的y坐标list
    """
    xs = [0] * 3
    ys = [0] * 3
    xs[1], ys[1] = points[0]
    xs[2], ys[2] = points[1]
    return xs, ys


def draw_leg_rr_model(data_origin, data_after):
    fig, ax = plt.subplots()  # 建立图像
    plt.plot(data_origin[0], data_origin[1], color='black', label='original')
    plt.scatter(data_origin[0], data_origin[1], color='black')
    plt.plot(data_after[0], data_after[1], color='red', label='after')
    plt.scatter(data_after[0], data_after[1], color='blue')
    ax.set(xlabel='X', ylabel='Y', title='mini pupper FK RR model')
    ax.grid()
    plt.axis("equal")
    plt.legend(loc=2)

    
def annotate_angle(x0, y0, rad1, rad2, name, inverse=False):
    """
    为两条直线绘制角度
    :param x0: 圆心x坐标
    :param y0: 圆心x坐标
    :param rad1: 起始角
    :param rad2: 终止角
    :param name: 角名
    :param inverse: 用于解决点1的重叠问题
    :return: 无
    """
    theta = np.linspace(rad1, rad2, 100)  # 0~rad
    r = 0.3  # circle radius
    x1 = r * np.cos(theta) + x0
    y1 = r * np.sin(theta) + y0
    plt.plot(x1, y1, color='red')
    plt.scatter(x0, y0, color='blue')
    degree = degrees((rad2 - rad1))
    if inverse:
        plt.annotate("%s=%.1f°" % (name, degree), [x0, y0], [x0 - r / 1.5, y0 - r / 1.5])
    else:
        plt.annotate("%s=%.1f°" % (name, degree), [x0, y0], [x0 + r / 1.5, y0 + r / 1.5])


# 关节信息
# 大臂长度：5 cm 小臂长度：6 cm
link_length = [5, 6]  # in cm

# 关节角初始化
joints_angle_origin = [-150, 90]
joints_angle = [0, 0]
print("关节角初始状态 theta1=%d°， theta2=%d°" % (joints_angle_origin[0], joints_angle_origin[1]))

# 输入连杆参数：各关节角
for i in range(1, 3):
    joints_angle[i - 1] = int(input("请输入腿部舵机[%d]要转动的的角度：" % i))
    print("腿部舵机[{0}]将转动{1}°".format(i, joints_angle[i - 1]))

# 计算并预处理绘图数据
points_origin = theta_2_position_rr(link_length[0], link_length[1], joints_angle_origin[0], joints_angle_origin[1])
points_after = theta_2_position_rr(link_length[0], link_length[1], joints_angle[0], joints_angle[1])
data_origin = preprocess_drawing_data(points_origin)
data_after = preprocess_drawing_data(points_after)

# 绘制模型
draw_leg_rr_model(data_origin, data_after)
# 标注
annotate_angle(data_origin[0][0], data_origin[1][0],
            0, radians(joints_angle_origin[0]), "theta1_original", inverse=True)
annotate_angle(data_origin[0][1], data_origin[1][1], radians(joints_angle_origin[0]),
            radians(joints_angle_origin[0] + joints_angle_origin[1]), "theta2_original", inverse=True)
annotate_angle(data_after[0][0], data_after[1][0],
            0, radians(joints_angle[0]), "theta1_after")
annotate_angle(data_after[0][1], data_after[1][1], radians(joints_angle[0]),
            radians(joints_angle[0] + joints_angle[1]), "theta2_after")
plt.show()

