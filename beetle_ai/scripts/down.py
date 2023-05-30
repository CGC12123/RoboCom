#encoding: UTF-8
from GrabParams import grabParams
from pymycobot.mycobot import MyCobot
import basic

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

basic.grap(False)
mc.set_color(0,255,0)#调节结束，亮绿灯