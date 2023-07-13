#encoding: UTF-8
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import os
import basic
import time
from GrabParams import grabParams

# 运行至初始位置
mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

# 往回收一下 防止撞到
coords_ori = grabParams.coords_right_high
coords_target = [coords_ori[0],  coords_ori[1] + 20, coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]
mc.send_coords(coords_target, 50, 0)
time.sleep(0.2)

mc.set_color(0, 255, 255)  #运行，亮蓝灯
mc.send_coords(grabParams.coords_right_low, 70, 0)


basic.grap(False)
mc.set_color(0, 255, 0)  #调节结束，亮绿灯
