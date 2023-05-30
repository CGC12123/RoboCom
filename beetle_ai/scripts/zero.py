from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams


mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
mc.set_color(0,0,255)#blue, arm is busy   

mc.send_angles([0,0,0,0,0,0],30)
time.sleep(6)

mc.set_color(0,255,0)#green, arm is free
