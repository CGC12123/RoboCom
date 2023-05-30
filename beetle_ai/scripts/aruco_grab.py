from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def aruco_grab():
    os.system(
        "python /home/robuster/beetle_ai/scripts/aruco_grab_2.py  --debug ''"
    )

t = threading.Thread(target=aruco_grab,name='aruco_grab')
t.setDaemon(True)
t.start()