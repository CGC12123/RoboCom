from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def grab_low():
    os.system(
        "python /home/robuster/beetle_ai/scripts/grab_low2.py  --debug ''"
    )

t = threading.Thread(target=grab_low,name='grab_low')
t.setDaemon(True)
t.start()