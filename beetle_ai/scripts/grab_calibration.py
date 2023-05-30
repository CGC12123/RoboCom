#encoding: UTF-8
#!/usr/bin/env python2
import cv2 as cv
import os
import numpy as np
import time
# import rospy
from pymycobot.mycobot import MyCobot
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic



class Detect_marker(object):

    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on() 

        self.cap = FastVideoCapture(grabParams.cap_num)

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

        # The coordinates of the cube relative to the mycobot
        self.c_x, self.c_y = grabParams.IMG_SIZE/2, grabParams.IMG_SIZE/2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio

        self.coords = grabParams.coords_ready

        self.done = grabParams.done

        self.size = 0;
   

    # set parameters to calculate the coords between cube and mycobot
    def get_ratio(self):
        self.ratio = 21.0/self.size
        print("self.ratio", self.ratio)
        return self.ratio



    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        basic.grap(False)      
        time.sleep(1)      
        basic.move_to_target_coords(self.coords,20)

    def show_image(self, img):
        cv.imshow("figure", img)
        cv.waitKey(50) 

    def get_position_size(self, corner):
        x1 = corner[0][0]
        x2 = corner[1][0]
        x3 = corner[2][0]
        y1 = corner[0][1]
        y2 = corner[1][1]
        y3 = corner[2][1]
        dx12 = x1-x2
        dx23 = x2-x3
        dy12 = y1-y2
        dy23 = y2-y3
        l1 = math.sqrt(dx12*dx12+dy12*dy12)
        l2 = math.sqrt(dx23*dx23+dy23*dy23)
        size = (l1+l2)*0.5
        return size
        
    def detect_aruco(self, img):
        # transfrom the img to model of gray
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Detect ArUco marker.
        corners, ids, rejectImaPoint = cv.aruco.detectMarkers(
            gray, self.aruco_dict, parameters=self.aruco_params
        )

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
                # print rvec.shape[0]

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
                    self.size = self.get_position_size(corners[i][0])

if __name__ == "__main__":

    
    detect = Detect_marker()
    detect.run()   

    count = 0
    ratio = 0

    while 1:
        # read camera
        img = detect.cap.read()
        img = cv.flip(img , 0)
        img = cv.flip(img , 1)
        detect.show_image(img)       
        detect.detect_aruco(img)
        if detect.size > 0:
            detect.get_ratio()
            ratio += detect.ratio
            count = count + 1
        if count >=20:
            detect.mc.set_color(0,255,0)#green, arm is free
            ratio = ratio/20
            print("ratio: ",ratio)
            print("hi man, ok now, please modify the ratio in GrabParams.py")
            break
        time.sleep(0.5)


   