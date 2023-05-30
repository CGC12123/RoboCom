from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
from GrabParams import grabParams
import basic
import os

print("stop arm.")
mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
angles = basic.get_angles()
mc.send_angles(angles,1)

