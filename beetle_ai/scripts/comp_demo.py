#encoding: UTF-8
#!/usr/bin/env python2
import time
from pymycobot.mycobot import MyCobot
from GrabParams import grabParams
import basic
mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
coords_top = [110.1, 0, 345, -90, 50+90, -90]
coords_bottom = [coords_top[0], coords_top[1], coords_top[2]-100, coords_top[3], coords_top[4],
coords_top[5]]
mc.set_color(0,0,255)#机械臂 LED 灯显示蓝色，表示正在工作
while 1:
	#机械臂移动到上层货架，抓取积木
	basic.grap(False) #张开夹爪
	mc.send_coords(coords_top,20,0)
	time.sleep(10)
	basic.grap(True)#闭合夹爪
	#机械臂移动右方，放置积木
	angles = [-87.27, 0, 0, 0, 0, 0]
	mc.send_angles(angles,25)
	time.sleep(3)
	angles = [-87.27, -45.26, 2.28, 1.66, -0.96, 47.02]
	mc.send_angles(angles,25)
	time.sleep(5)
	basic.grap(False)
	#机械臂移动到下层货架，抓取积木
	basic.grap(False)
	mc.send_coords(coords_bottom,20,0)
	time.sleep(10)
	basic.grap(True)
	#机械臂移动右方，放置积木
	angles = [-87.27, 0, 0, 0, 0, 0]
	mc.send_angles(angles,25)
	time.sleep(3)
	angles = [-87.27, -45.26, 2.28, 1.66, -0.96, 47.02]
	mc.send_angles(angles,25)
	time.sleep(5)
	basic.grap(False)