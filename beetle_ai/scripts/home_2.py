#encoding: UTF-8
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
import basic
from GrabParams import grabParams

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.set_color(0,0,255)#运行，亮蓝灯

angles = [0, 0, 0, 0, 0, 45]
mc.send_angles(angles,70)
time.sleep(1)

angles = [-83.23, -140.53, 140.97, 58.71, -127.61, 5.71]
mc.send_angles(angles,20)
time.sleep(1)

mc.set_color(0,255,0)#调节结束，亮绿灯

