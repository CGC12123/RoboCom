from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def grab_right():
    os.system(
        "python /home/robuster/beetle_ai/scripts/grab_right2.py  --debug ''  "
    )

t = threading.Thread(target=grab_right,name='grab_right')
t.setDaemon(True)
t.start()