#!/usr/bin/python
# coding:utf-8
# vector_rotation.py
# 使参考坐标系内的一指定向量绕x、y、z轴旋转指定角度，并依次按红、橙、绿、蓝绘制出原向量和旋转后的向量
import matplotlib.pyplot as plt  # 引入matplotlib库
import numpy as np  # 引入numpy库


def rotate_X(x, y, z, alpha):
    alpha = alpha * (np.pi / 180)
    x_r = x
    y_r = np.cos(alpha)*y - np.sin(alpha)*z
    z_r = np.sin(alpha)*y + np.cos(alpha)*z
    print(f"Test_X-axis:{(x, y, z)} rotate {alpha*(180/np.pi)} degrees,result: {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

def rotate_Y(x, y, z, beta):
    beta = beta * (np.pi / 180)
    x_r = np.cos(beta)*x + np.sin(beta)*z
    y_r = y
    z_r = -np.sin(beta)*x + np.cos(beta)*z
    print(f"Test_Y-axis:{(x, y, z)} rotate {alpha*(180/np.pi)} degrees,result: {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

def rotate_Z(x, y, z,  gamma):
    gamma = gamma * (np.pi / 180)
    x_r = np.cos(gamma)*x - np.sin(gamma)*y
    y_r = np.sin(gamma)*x + np.cos(gamma)*y
    z_r = z
    print(f"Test_Z-axis:{(x, y, z)} rotate {alpha*(180/np.pi)} degrees,result: {(x_r, y_r, z_r)}")
    return x_r, y_r, z_r

def draw_before(px,py,pz):
    x_vector = ax.quiver(origin[0], origin[1], origin[2],
                         ac2 * x_axis_unit_vector[0], ac2 * x_axis_unit_vector[1], ac2 * x_axis_unit_vector[2],
                         arrow_length_ratio=0.1, color="black")  # 绘制A坐标系的x单位向量
    y_vector = ax.quiver(origin[0], origin[1], origin[2],
                         ac2 * y_axis_unit_vector[0], ac2 * y_axis_unit_vector[1], ac2 * y_axis_unit_vector[2],
                         arrow_length_ratio=0.1, color="black")  # 绘制A坐标系的y单位向量
    z_vector = ax.quiver(origin[0], origin[1], origin[2],
                         ac2 * z_axis_unit_vector[0], ac2 * z_axis_unit_vector[1], ac2 * z_axis_unit_vector[2],
                         arrow_length_ratio=0.1, color="black")  # 绘制A坐标系的z单位向量
    p_vector = ax.quiver(origin[0], origin[1], origin[2],
                         px, py, pz,
                         arrow_length_ratio=0.1, color="red")  # 绘制A坐标系的p向量
    print(px, py, pz)

# plot_init
fig = plt.figure() # 建立图像
ax = fig.add_subplot(projection="3d")  # 为图像添加三维坐标系
#ax.grid(False)  # 取消网格线，如需要网格线，请注释该行
# Setting the axes properties
ax.set(xlim3d=(0, 5), xlabel='X')
ax.set(ylim3d=(0, 5), ylabel='Y')
ax.set(zlim3d=(0, 5), zlabel='Z')

# variable_init
origin = [0, 0, 0]
x_axis_unit_vector = [1, 0, 0]
y_axis_unit_vector = [0, 1, 0]
z_axis_unit_vector = [0, 0, 1]
# ac = 6  # 坐标轴底色向量增益系数
ac2 = 4  # A坐标系增益系数

# # 绘制坐标轴底色向量
# ax.quiver(origin[0], origin[1], origin[2],
#           ac*x_axis_unit_vector[0], ac*x_axis_unit_vector[1], ac*x_axis_unit_vector[2],
#           arrow_length_ratio=0.1, color="black")  # 绘制x方向底色向量
# ax.quiver(origin[0], origin[1], origin[2],
#           ac*y_axis_unit_vector[0], ac*y_axis_unit_vector[1], ac*y_axis_unit_vector[2],
#           arrow_length_ratio=0.1, color="black")  # 绘制y方向底色向量
# ax.quiver(origin[0], origin[1], origin[2],
#           ac*z_axis_unit_vector[0], ac*z_axis_unit_vector[1], ac*z_axis_unit_vector[2],
#           arrow_length_ratio=0.1, color="black")  # 绘制z方向底色向量

vector_in_A_pre= input("请分别输入该向量在参考坐标系A中的xyz分量，以空格隔开：")
vector_in_A = [int(n) for n in vector_in_A_pre.split()]
print("向量相对参考坐标系：", vector_in_A)
rotate_pre= input("请输入向量绕参考坐标系x轴、y轴、z轴依次旋转的角度(角度制)：") # 旋转采用Fixed Angles模式
rotate = [int(n) for n in rotate_pre.split()]
print("向量分别绕x,y,z轴：", rotate)
alpha = rotate[0]
beta = rotate[1]
gamma = rotate[2]

draw_before(vector_in_A[0], vector_in_A[1], vector_in_A[2]) # 绘制原坐标系及原指定向量

first_vector = rotate_X(vector_in_A[0], vector_in_A[1], vector_in_A[2],alpha)
p1_vector = ax.quiver(origin[0], origin[1], origin[2],
                     first_vector[0], first_vector[1], first_vector[2],
                     arrow_length_ratio=0.1, color="orange")  # 绘制绕x旋转后的p向量
second_vector = rotate_Y(first_vector[0], first_vector[1], first_vector[2],beta)
p2_vector = ax.quiver(origin[0], origin[1], origin[2],
                     second_vector[0], second_vector[1], second_vector[2],
                     arrow_length_ratio=0.1, color="green")  # 绘制绕y旋转后的p向量
third_vector = rotate_Z(second_vector[0], second_vector[1], second_vector[2],gamma)
p3_vector = ax.quiver(origin[0], origin[1], origin[2],
                     third_vector[0], third_vector[1], third_vector[2],
                     arrow_length_ratio=0.1, color="blue")  # 绘制绕z旋转后的p向量

plt.show()  # 绘制
