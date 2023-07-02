#encoding: UTF-8
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import os
import basic
from GrabParams import grabParams

# 运行至初始位置
mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.set_color(0, 255, 255)  #运行，亮蓝灯
mc.send_coords(grabParams.coords_right_high, 70, 0)

basic.grap(False)
mc.set_color(0, 255, 0)  #调节结束，亮绿灯
