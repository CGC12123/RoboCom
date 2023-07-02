#encoding: UTF-8
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import os, time
import basic
from GrabParams import grabParams

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

coords_ori = grabParams.coords_left_low

# coords_target_2 = [coords_ori[0], coords_ori[1], coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]

coords_target_2 = [coords_ori[0], coords_ori[1] + grabParams.bias_left_low_y, coords_ori[2] + grabParams.bias_left_low_z, coords_ori[3], coords_ori[4], coords_ori[5]]

mc.send_coords(coords_target_2, 70, 0)
time.sleep(0.4)
# 移动到目标位置
# coords_target_2 = [coords_ori[0] + grabParams.bias_left_high_x,  coords_ori[1] + 50,
#                    coords_ori[2] + grabParams.bias_left_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
# mc.send_coords(coords_target_2, 70, 0)
# time.sleep(1)

# mc.set_color(0, 255, 255)  #运行，亮蓝灯
# mc.send_coords(grabParams.coords_left_high_pitch, 70, 0)

# basic.grap(False)
# mc.set_color(0, 255, 0)  #调节结束，亮绿灯
