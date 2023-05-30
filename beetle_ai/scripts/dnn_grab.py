from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def dnn_grab():
    os.system(
        "python /home/robuster/beetle_ai/scripts/dnn_grab_2.py  --debug ''"
    )

t = threading.Thread(target=dnn_grab,name='dnn_grab')
t.setDaemon(True)
t.start()