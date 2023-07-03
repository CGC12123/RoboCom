# -*- coding: UTF-8 -*-
import subprocess
import time
import os

# 导航目标点请在 bash/Start2.sh中修改

# 打开导航软件
sh1s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Start1.sh",
        "/home/robuster/RoboCom/navigation/bash/Start1.sh"]
sh1 = "bash -c '{}'".format("; ".join(sh1s))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(10) # 等待导航程序启动完成

# 发布目标地点话题
sh2s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Start2.sh",
        "/home/robuster/RoboCom/navigation/bash/Start2.sh"]
sh2 = "bash -c '{}'".format("; ".join(sh2s))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 运行下一步自动夹取
sh3s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Grab.sh",
        "/home/robuster/RoboCom/navigation/bash/Grab.sh"]
sh3 = "bash -c '{}'".format("; ".join(sh3s))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh3, '--hold'], 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)