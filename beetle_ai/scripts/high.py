#encoding: UTF-8
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import os
import basic
from GrabParams import grabParams

if os.path.exists("/home/robuster/beetle_ai/scripts/direction.txt"):
    f = open("/home/robuster/beetle_ai/scripts/direction.txt", "r")
    direction = int(f.read())
    f.close()
else:
    f = open("/home/robuster/beetle_ai/scripts/direction.txt", "w")
    f.write('0')
    direction = 0
    f.close()

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.set_color(0,255,255)#运行，亮蓝灯

if direction:  
    mc.send_coords(grabParams.coords_high_right, 70, 0)
    f = open("/home/robuster/beetle_ai/scripts/direction.txt", "w")
    f.write('0')
    f.close()
else:
    mc.send_coords(grabParams.coords_high_left, 70, 0)
    f = open("/home/robuster/beetle_ai/scripts/direction.txt", "w")
    f.write('1')
    f.close()

basic.grap(False)
mc.set_color(0,255,0)#调节结束，亮绿灯

