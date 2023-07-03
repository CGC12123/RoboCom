import subprocess
import time

# 导航目标点请在 bash/Start2.sh中修改

sh1 = "" # 使用绝对路径
sh2 = ""
# 打开导航软件
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(5) # 等待导航程序启动完成

# 发布目标地点话题
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)