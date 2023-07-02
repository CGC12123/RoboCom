from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def grab_left_low():
    os.system(
        "python /home/robuster/RoboCom/beetle_ai/scripts/grab_left_low2.py  --debug ''  "
    )

t = threading.Thread(target=grab_left_low,name='grab_left_low')
t.setDaemon(True)
t.start()