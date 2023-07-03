# -*- coding: UTF-8 -*-
import subprocess
import time
import os

# 回到出发点
# 导航目标点请在 bash/Back.sh中修改

# 发布目标地点话题
sh2s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Back.sh",
        "/home/robuster/RoboCom/navigation/bash/Back.sh"]
sh2 = "bash -c '{}'".format("; ".join(sh2s))
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)