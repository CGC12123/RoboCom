# -*- coding: UTF-8 -*-
import subprocess
import time
import os
import signal
def t():
    sh2s = ["/home/robuster/RoboCom/navigation/bash/Start2.sh"]
    sh2 = "bash -c '{}'".format("; ".join(sh2s))
    process = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = process.pid
    time.sleep(15)
    os.kill(pid, signal.SIGINT)  # 终止进程
    # process.terminate()
    # process.kill()
    # os.system("sudo kill -9 {}".format(pid))
    # 获取新进程的 PID 并打印

pid = t()
print("New process PID:", pid)
# time.sleep(15)
# os.kill(pid, signal.SIGINT)  # 终止进程
# process.terminate()