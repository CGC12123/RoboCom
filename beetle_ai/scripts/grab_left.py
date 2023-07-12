from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def grab_left():
    os.system(
        "python /home/robuster/RoboCom/beetle_ai/scripts/grab_left2.py  --debug ''  "
    )

def grab_left_low():
    os.system(
        "python /home/robuster/RoboCom/beetle_ai/scripts/grab_left_low2.py  --debug ''  "
    )

f = open("/home/robuster/RoboCom/beetle_ai/scripts/direction.txt", "r")
direction = int(f.read())

if direction:
    t = threading.Thread(target=grab_left_low,name='grab_left_low')
    t.setDaemon(True)
    t.start()

else:
    t = threading.Thread(target=grab_left,name='grab_left')
    t.setDaemon(True)
    t.start()