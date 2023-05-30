#encoding: UTF-8
#!/usr/bin/env python2
import cv2 as cv
import os
import numpy as np
import time
from pymycobot.mycobot import MyCobot
from VideoCapture import FastVideoCapture
import math
import rospy
from geometry_msgs.msg import Twist

done = False
cap_num = 2
usb_dev = "/dev/arm"


# show image and waitkey
debug = True 

class Follow_aruco(object):
    def __init__(self):
        super(Follow_aruco, self).__init__()

        rospy.init_node('follow_aruco', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(20) # 10hz
        

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
        self.ratio = 0.25
    
   

    # calculate the coords between cube and robot
    def get_position(self, corners):
        x = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
        y = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]
        x = x/4.0
        y = y/4.0
        x_size_p = abs(x - corners[0][0][0][0])*2
        y_size_p = abs(y - corners[0][0][0][1])*2
        return (-(x - self.c_x)), (-(y - self.c_y)), x_size_p, y_size_p


    def show_image(self, img):
        if debug:
            cv.imshow("figure", img)
            cv.waitKey(50) 

    def send_cmd_vel(self, x, y, xsize , ysize):
        move_cmd = Twist()      

        if xsize > 130 or ysize > 130:
            global done
            done = True
            self.pub.publish(Twist())
        elif xsize > 100 or ysize > 100:
            move_cmd.linear.x = 0.05
            if abs(x) > 1:
                move_cmd.angular.z = x/self.cap.getWidth()
            self.pub.publish(move_cmd)
        else:
            move_cmd.linear.x = 0.15
            if abs(x) > 1:
                move_cmd.angular.z = x/self.cap.getWidth()
            self.pub.publish(move_cmd)
        self.rate.sleep()
        print(move_cmd.linear.x, move_cmd.angular.z)


    def run(self):     

       
        while not done:
            img = self.cap.read()
            
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
                        # self.show_image(img)
                        # print(corners)
                        real_x, real_y, xsize, ysize = detect.get_position(corners)
                        print(real_x, real_y, xsize, ysize)

                        self.send_cmd_vel(real_x, real_y, xsize, ysize)

                        print(time.time())


                                                    
                            

            self.show_image(img)
        cv.destroyAllWindows()
        

if __name__ == "__main__":    
    detect = Follow_aruco()
    detect.run()

