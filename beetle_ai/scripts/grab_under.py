from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def grab_under():
    os.system(
        "python /home/robuster/RoboCom/beetle_ai/scripts/grab_under2.py  --debug ''  "
    )

t = threading.Thread(target=grab_under,name='grab_under')
t.setDaemon(True)
t.start()