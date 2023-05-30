from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams
import basic

x_bias = 60
y_bias = 30
z_bias = 0
r_bias = -90
h = 250.7
# h = 350.7

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
mc.set_color(0,0,255)#blue, arm is busy   

# coords = basic.get_coords()
# print(coords)

angles = basic.get_angles()
print(angles)

# angles = [86.83, -50.44, -8.17, 47.98, -88.5, 146.6] #1
# mc.send_angles(angles,10)
# time.sleep(10)

# angles = [86.22, -40.69, -20.83, 111.79, -86.92, 86.39] #2
# mc.send_angles(angles,10)
# time.sleep(10)

# angles = [92.98, -38.58, 39.81, 73.56, -92.28, 56.77] #3
# mc.send_angles(angles,10)
# time.sleep(10)

# angles = [97.03, -7.38, 40.69, 46.14, -95.62, 53.08] #4
# mc.send_angles(angles,10)
# time.sleep(10)

# angles = [93.86, 55.19, -9.93, -3.42, -89.47, 92.28] #5
# mc.send_angles(angles,10)
# time.sleep(10)

# coords = [108.8, -6.3, 329.8, 90.95, 44.73, 88.72] #3
# mc.send_coords(coords,15,0)
# time.sleep(10)
# coords = [105.3, -101.2, 340.2, 89.87, 46.75, 87.81]
# mc.send_coords(coords,15,0)

# close
# mc.set_gripper_value(255,25)
# time.sleep(2)

# coords_top = [110.1, 0, 345, -90, 50+90, -90]

# coords = [coords_top[0], coords_top[1], coords_top[2]-100, coords_top[3], coords_top[4], coords_top[5]]

# coords = [170, -55, 270, -179, 2, -135]
# mc.send_coords(coords,15,0)
# time.sleep(15)

# mc.set_gripper_value(255,25)
# time.sleep(2)

# mc.send_coords([coords[0]+30, coords[1]+60, coords[2], coords[3], coords[4], coords[5]],15,0)
# time.sleep(6)

# mc.set_gripper_value(40,25)
# time.sleep(2)


# mc.send_coords([coords[0]+x_bias, coords[1]+y_bias, coords[2]+z_bias, coords[3], coords[4]+r_bias, coords[5]],15,0)
# time.sleep(5)
# # mc.send_coords([coords[0]+x_bias, coords[1]+y_bias, coords[2], coords[3], coords[4]+r_bias, coords[5]],15,0)
# # time.sleep(2)

# # # open
# mc.set_gripper_value(255,20)
# time.sleep(1)

# dy = 0
# while 1:
# 	if dy > -100:
# 		dy -= 5
# 		print("dy: "+str(dy))
# 	else: 
# 		break
# 	mc.send_coords([120.1, -50.4+dy, 350.7, -91.6, 45, -89.04],15,1)
# 	time.sleep(0.5)

# while 1:
# 	if dy < 100:
# 		dy += 5
# 		print("dy: "+str(dy))
# 	else: 
# 		break
# 	mc.send_coords([120.1, -50.4+dy, 350.7, -91.6, 45, -89.04],15,1)
# 	time.sleep(0.5)

# mc.set_color(0,255,0)#green, arm is free
