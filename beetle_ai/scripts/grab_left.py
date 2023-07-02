from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def grab_left():
    os.system(
        "python /home/robuster/RoboCom/beetle_ai/scripts/grab_left2.py  --debug ''  "
    )

t = threading.Thread(target=grab_left,name='grab_left')
t.setDaemon(True)
t.start()