from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
import basic
from GrabParams import grabParams

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.set_color(0,0,255)#blue, arm is busy   

angles = [0, 0, 0, 0, 0, 0]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-83.23, -140.53, 140.97, 58.71, -127.61, 5.71]
mc.send_angles(angles,25)
time.sleep(6)

mc.set_color(0,255,0)#green, arm is free

mc.release_all_servos()
mc.power_off()


