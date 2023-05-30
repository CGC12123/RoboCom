#encoding: UTF-8
#!/usr/bin/env python2
import cv2 as cv
import os
import numpy as np
import time
from pymycobot.mycobot import MyCobot
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()


# y轴偏移量
y_bias = grabParams.y_bias #40
# x轴偏移量
x_bias = grabParams.x_bias #5
# rotation
rotation_angle = 0
#height
height_bias = grabParams.height_bias
done = grabParams.done
cap_num = grabParams.cap_num


# show image and waitkey
debug = grabParams.debug

coords = grabParams.coords_ready 


class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()

        self.mc.set_color(0,0,255)#blue, arm is busy 

        # Creating a Camera Object
        self.cap = FastVideoCapture(cap_num)
        # Get ArUco marker dict that can be detected.
        self.aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
        # Get ArUco marker params.
        self.aruco_params = cv.aruco.DetectorParameters_create()
        self.calibrationParams = cv.FileStorage("calibrationFileName.xml", cv.FILE_STORAGE_READ)
        # Get distance coefficient.
        self.dist_coeffs = self.calibrationParams.getNode("distCoeffs").mat()

        height = self.cap.getHeight()
        focal_length = width = self.cap.getWidth()
        center = [width / 2, height / 2]
        # Calculate the camera matrix.
        self.camera_matrix = np.array(
            [
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1],
            ],
            dtype=np.float32,
        )
        self.c_x, self.c_y = width/2, height/2

        self.ratio = grabParams.ratio
        
    

    # Grasping motion
    def move(self, x, y):
        global height_bias, done
        coords_target = [coords[0]+int(x), coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(coords_target, grabParams.GRAB_MOVE_SPEED)
       

        basic.grap(True)

        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        time.sleep(3)

        done = True
        print("Done")
        self.mc.set_color(0,255,0)#green, arm is free


    # init mycobot
    def init_mycobot(self): 
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        basic.grap(False)      
        time.sleep(1)         
        basic.move_to_target_coords(coords,grabParams.GRAB_MOVE_SPEED)  
        

       

    def rotate_ange(self):

        angles = self.mc.get_angles()
        while len(angles)<6:
            angles = self.mc.get_angles()
            # print angles
        # print angles
        axis6 = angles[5]
        # print "axis6:"
        # print axis6
        ang = axis6 - rotation_angle #consider the initial angele of axix 6 
        # print ang
        self.mc.send_angle(6,ang,50)
        time.sleep(1.5)
    
    def reset_rotate_ange(self):
        self.mc.send_angle(6,90,60)
        time.sleep(1)
        
    def get_rotation(self,corners):
        # print corners
        xy = corners[0][0][0,:] - corners[0][0][1,:]
        # print xy
        ang = math.atan2(xy[0],xy[1])*57.3
        # print ang
        ang = self.get_correct_angle(ang)
        # print ang
        return ang
    
    def get_correct_angle(self, ang):
        if(abs(ang) < 45):
            return ang
        else:
            if(ang < 0):
                ang = ang + 90
            else:
                ang = ang - 90
            return self.get_correct_angle(ang)

    # calculate the coords between cube and mycobot
    def get_position(self, corners):
        x = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
        y = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]
        x = x/4.0
        y = y/4.0
        wx = wy = 0
        if grabParams.grab_direct == "front":
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x) * self.ratio
        elif grabParams.grab_direct == "right":
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio
        return wx, wy
            


    def show_image(self, img):
        if debug and args.debug:
            cv.imshow("figure", img)
            cv.waitKey(50) 

    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        global y_bias, x_bias, rotation_angle
        self.init_mycobot()
        num = sum_x = sum_y = 0 
        count = 1
        while cv.waitKey(1)<0 and not done:
            img = self.cap.read()
            img = cv.flip(img,0)
            img = cv.flip(img,1)
            # if not success:
            #     print("It seems that the image cannot be acquired correctly.")
            #     break
            
            # transfrom the img to model of gray
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # Detect ArUco marker.
            corners, ids, rejectImaPoint = cv.aruco.detectMarkers(
                gray, self.aruco_dict, parameters=self.aruco_params
            )

            # print corners, len(corners)

            if len(corners) > 0:                
                if ids is not None:
                    # get informations of aruco
                    ret = cv.aruco.estimatePoseSingleMarkers(
                        corners, 0.021, self.camera_matrix, self.dist_coeffs
                    )
                    # rvec:rotation offset,tvec:translation deviator
                    (rvec, tvec) = (ret[0], ret[1])
                    (rvec - tvec).any()
                    
                    # print corners

                    for i in range(rvec.shape[0]):
			            # draw the aruco on img
                        cv.aruco.drawDetectedMarkers(img, corners)
                        cv.aruco.drawAxis(
                            img,
                            self.camera_matrix,
                            self.dist_coeffs,
                            rvec[i, :, :],
                            tvec[i, :, :],
                            0.03,
                        )
                        self.show_image(img)
                        # print(corners)
                        real_x, real_y = detect.get_position(corners)

                        # print(real_x, real_y)
                        if num < count:
                            sum_x += real_x
                            sum_y += real_y
                            num += 1
                        elif num ==count:
                            coords_now = basic.get_coords()
                            if len(coords_now) == 6:
                                coords = coords_now
                            # rotation_angle = self.get_rotation(corners)                                                         
                            print(sum_x/count, sum_y/count)
                            self.move(sum_x/count+x_bias, sum_y/count+y_bias)
                            num = sum_x = sum_y = 0  
                            self.cap.close() 
                                                    
                            

            self.show_image(img)

        

if __name__ == "__main__":    
    detect = Detect_marker()
    detect.run()

