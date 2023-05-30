from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def grab_high():
    os.system(
        "python /home/robuster/beetle_ai/scripts/grab_high2.py  --debug ''  "
    )

t = threading.Thread(target=grab_high,name='grab_high')
t.setDaemon(True)
t.start()