from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams
import basic


mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_off()