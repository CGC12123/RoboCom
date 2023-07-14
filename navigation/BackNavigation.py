# -*- coding: UTF-8 -*-
import subprocess
import time
import os
import signal

# 回到出发点
# 导航目标点请在 bash/Back.sh中修改
# 打开文件
with open('/home/robuster/RoboCom/navigation/pid.txt', 'r') as file:
    # 读取文件内容
    pid = file.read()
    # 打印文件内容
    print(pid)
os.kill(pid, signal.SIGINT)  # 终止进程

# 打开导航软件
sh1s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Start1.sh",
                "/home/robuster/RoboCom/navigation/bash/Start1.sh"]
sh1 = "bash -c '{}'".format("; ".join(sh1s))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], 
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(15) # 等待导航程序启动完成

sh1s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Start1.sh",
                "/home/robuster/RoboCom/navigation/bash/Start1.sh"]
sh1 = "bash -c '{}'".format("; ".join(sh1s))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], 
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(15) # 等待导航程序启动完成

# 发布目标地点话题
sh2s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Back.sh",
        "/home/robuster/RoboCom/navigation/bash/Back.sh"]
sh2 = "bash -c '{}'".format("; ".join(sh2s))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)