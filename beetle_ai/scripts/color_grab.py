from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def color_grab():
    os.system(
        "python /home/robuster/beetle_ai/scripts/color_grab_2.py  --debug ''"
    )

t = threading.Thread(target=color_grab,name='color_grab')
t.setDaemon(True)
t.start()