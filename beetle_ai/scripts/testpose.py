from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams
import basic

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

mc.set_color(0,0,255)#blue, arm is busy   

coords = [203.6, -56.4, 240.9, -178.34, 2.93, -133.7]
basic.move_to_target_coords(coords, 20)

mc.set_color(0,255,0)#green, arm is free
