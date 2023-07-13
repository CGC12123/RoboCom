#encoding: UTF-8
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import os, time
import basic
from GrabParams import grabParams

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

x = 0

# 防止离太近 先收回来
coords_ori = grabParams.coords_right_high
coords_target = [coords_ori[0] + x,  coords_ori[1] + 30,  coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]
mc.send_coords(coords_target, 50, 0)
time.sleep(0.5)
coords_ori = grabParams.coords_right_high
coords_target = [coords_ori[0] + x,  coords_ori[1] + 30,  coords_ori[2] + 60, coords_ori[3], coords_ori[4], coords_ori[5]]
mc.send_coords(coords_target, 50, 0)
time.sleep(0.5)

# 为了防止卡死先对位置 并往回收防止撞到
coords_target_2 = [coords_ori[0] + grabParams.bias_right_high_x + x,  coords_ori[1] - 10,  
                    coords_ori[2] + grabParams.bias_right_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
mc.send_coords(coords_target_2, 50, 0)
time.sleep(0.5) # 等它先到平面上
# 移动到目标位置 往前推
coords_target_3 = [coords_ori[0] + grabParams.bias_right_high_x + x,  coords_ori[1] + grabParams.bias_right_high_y,  
                    coords_ori[2] + grabParams.bias_right_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
mc.send_coords(coords_target_3, 30, 0)
time.sleep(0.8)
basic.grap(True)
time.sleep(1)

# 放回
mc.send_coords(grabParams.coords_pitchdown1, 50, 0) # 先抬高
time.sleep(0.5)
mc.send_coords(grabParams.coords_pitchdown2, 50, 0)
time.sleep(1)
basic.grap(False)
done = True
time.sleep(1)

mc.set_color(0,255,0) #抓取结束，亮绿灯
os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right.py")
# 移动到目标位置
# coords_target_2 = [coords_ori[0] + grabParams.bias_left_high_x,  coords_ori[1] + 50,
#                    coords_ori[2] + grabParams.bias_left_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
# mc.send_coords(coords_target_2, 70, 0)
# time.sleep(1)

# mc.set_color(0, 255, 255)  #运行，亮蓝灯
# mc.send_coords(grabParams.coords_left_high_pitch, 70, 0)

# basic.grap(False)
# mc.set_color(0, 255, 0)  #调节结束，亮绿灯
