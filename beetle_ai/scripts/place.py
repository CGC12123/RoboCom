from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def place():
    os.system(
        "python /home/robuster/beetle_ai/scripts/place_2.py"
    )

t = threading.Thread(target=place,name='place')
t.setDaemon(True)
t.start()