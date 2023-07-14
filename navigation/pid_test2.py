# -*- coding: UTF-8 -*-
import subprocess
import os
import signal

# 启动新终端并发布话题
sh2s = ["/home/robuster/RoboCom/navigation/bash/Back.sh"]
sh2 = "bash -c '{}'".format("; ".join(sh2s))
process = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 获取新进程的 PID 并打印
bash_pid = process.pid
print("bash -c PID:", bash_pid)

# 查找子进程并发送 SIGINT 信号
output = subprocess.check_output(["ps", "-o", "pid,ppid,args"])
lines = output.decode().split("\n")
for line in lines:
    fields = line.split()
    if len(fields) >= 3 and fields[1] == str(bash_pid) and fields[2].endswith("Back.sh"):
        os.kill(int(fields[0]), signal.SIGINT)