from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

angular = 0 # linear  = 1

#grap
def grap(flag):
    if flag:
        # close
        mc.set_gripper_value(40,90)
    else:
        # open
        mc.set_gripper_value(255,90)

def move_to_target_coords(coords,speed):
    print("move_to_target_coords_2")
    mc.set_color(0,0,255)#blue, arm is busy
    mc.send_coords(coords,speed,angular)
    time.sleep(4)




def move_to_target_coords2(coords,speed):
    print("move_to_target_coords")
    mc.set_color(0,0,255)#blue, arm is busy
    time.sleep(0.1)
    mc.send_coords(coords,speed,angular)
    
    count = 0
    while 1:
        time.sleep(0.1)
        is_finised = mc.is_in_position(coords,1);
        print(is_finised)
        
        coords_now = mc.get_coords()
        if len(coords_now)<6:
            continue
        dx = coords_now[0] - coords[0]
        dy = coords_now[1] - coords[1]
        dz = coords_now[2] - coords[2]
        print(dx,dy,dz)
        if abs(dx) >4 or abs(dy)>4:
            continue
        else:
            count +=1            
            
            if count >= 5:
                print(coords)    
                print(coords_now)                
                break

def get_coords():
    coords_now = []
    count = 0
    while len(coords_now)<6 and count < 6:  
        time.sleep(0.5)            
        coords_now = mc.get_coords()        
        # print("get_coords ", coords_now, count)
        count = count + 1
        
    return coords_now


def get_angles():
    angles = mc.get_angles()
    while len(angles)<6:
        angles = mc.get_angles()
    return angles
