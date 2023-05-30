#encoding: UTF-8
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams


mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
mc.set_color(0,0,255)#运行，亮蓝灯  

mc.send_angles([0,0,0,0,0,45],70)
time.sleep(0.2)

mc.set_color(0,255,0)#调节结束，亮绿灯
