from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time

def home():
    os.system(
        "python /home/robuster/beetle_ai/scripts/home_2.py"
    )

t = threading.Thread(target=home(),name='home')
t.setDaemon(True)
t.start()