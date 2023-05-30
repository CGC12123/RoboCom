# encoding: UTF-8
# !/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo

from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
from geometry_msgs.msg import Twist
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()

done = False


class Detect_marker(object):

    def __init__(self):
        super(Detect_marker, self).__init__()

        rospy.init_node('Detect_marker', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(20)  # 20hz
        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()

        self.yolo = yolo()

        #self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        # Get ArUco marker params.
        #self.aruco_params = cv2.aruco.DetectorParameters_create()
        #self.calibrationParams = cv2.FileStorage("calibrationFileName.xml", cv2.FILE_STORAGE_READ)
        # Get distance coefficient.
        #self.dist_coeffs = self.calibrationParams.getNode("distCoeffs").mat()
        # parameters to calculate camera clipping parameters
        self.x1 = self.x2 = self.y1 = self.y2 = 0

        # use to calculate coord between cube and mycobot
        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0
        # The coordinates of the grab center point relative to the mycobot

        # The coordinates of the cube relative to the mycobot
        self.c_x, self.c_y = grabParams.IMG_SIZE / 2, grabParams.IMG_SIZE / 2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio

    # Grasping motion
    def move(self, y, d):
        global done
        self.mc.send_coords([coords[0], coords[1] + int(y), 258, 85, 45, 85], 80, 0)
        time.sleep(1.5)
        done = True
        print("Done")
        self.mc.set_color(0, 255, 0)  # green, arm is free
        t = abs(d) / 10
        # if abs(distance_to_center) > 1:
        move_cmd = Twist()
        move_cmd.linear.x = 0.10
        self.pub.publish(move_cmd)
        self.wait_cmd_vel(t, move_cmd)
        move_cmd = Twist()
        self.pub.publish(move_cmd)
        basic.grap(True)

    # calculate the coords between cube and robot
    def get_distance(self, corners):
        x = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
        y = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]
        x = x / 4.0
        y = y / 4.0
        x_size_p = abs(x - corners[0][0][0][0]) * 2
        y_size_p = abs(y - corners[0][0][0][1]) * 2
        # print (x)
        return (-(x - self.c_x)), (-(y - self.c_y)), x_size_p, y_size_p

    def move_back(self, d):
        t = abs(d) / 15
        # if abs(distance_to_center) > 1:
        move_cmd = Twist()
        move_cmd.linear.x = -0.15
        # self.pub.publish(move_cmd)
        self.wait_cmd_vel(t, move_cmd)
        move_cmd = Twist()
        self.pub.publish(move_cmd)
        angles = [84.28, -37.79, -17.22, 32.43, -18.1, 139.83]
        self.mc.send_angles(angles, 50)
        time.sleep(2)
        basic.grap(False)
        angles = [29.79, -139.48, 127.52, 18.1, -29.97, 130.86]
        self.mc.send_angles(angles, 50)

    def wait_cmd_vel(self, t, cmd_vel):
        count = t / 1
        while count > 0:
            self.pub.publish(cmd_vel)
            time.sleep(0.1)
            count = count - 1

            # init mycobot

    def init_mycobot(self):
        self.mc.send_coords([149.4, -13.6, 220.0, 85, 45, 85], 20, 0)
        basic.grap(False)

    # calculate the coords between cube and mycobot
    def get_position(self, y):
        wx = wy = 0
        wy = (self.c_y - y) * self.ratio
        return wy

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))

        return frame

    # detect object
    def obj_detect(self, img):
        x = y = 0
        # Load ONNX model
        print('--> Loading model')
        net = cv2.dnn.readNetFromONNX(grabParams.ONNX_MODEL)
        print('done')

        t1 = time.time()
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (grabParams.IMG_SIZE, grabParams.IMG_SIZE), [0, 0, 0], swapRB=True,
                                     crop=False)
        net.setInput(blob)
        t1 = time.time()
        # Inference
        print('--> Running model')
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

        # simple post process
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)

        print(classes)

        t2 = time.time()
        if boxes is not None:
            for i in classes:
                if i == 3:
                    classes = [i]
                    self.yolo.draw(img, boxes, scores, classes)
                    left, top, right, bottom = boxes[0]
                    y = int((left + right) / 2)
                    x = int((top + bottom) / 2)

        if x + y > 0:
            return x, y
        else:
            return None

    def run(self):
        self.mc.set_color(0, 0, 255)  # blue, arm is busy
        self.init_mycobot()

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(1000)


if __name__ == "__main__":

    detect = Detect_marker()
    detect.run()

    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5)
    #knownWidth = 24.5
    #focalLength = 550.5

    init_num = 0
    nparams = 0
    num = 0
    miss = 0
    while cv2.waitKey(1) < 0 and not done:
        # read camera
        frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect ArUco marker.
        corners, ids, rejectImaPoint = cv2.aruco.detectMarkers(gray, detect.aruco_dict, parameters=detect.aruco_params)
        # deal img
        frame = detect.transform_frame(frame)
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, 1)
        detect.show_image(frame)

        # get detect result
        detect_result = detect.obj_detect(frame)

        detect.show_image(frame)
        if detect_result is None:
            continue
        else:
            x, y = detect_result
            xsize, ysize = detect.get_distance(corners)
            d = 100
            real_y = detect.get_position(y)
            coords_now = basic.get_coords()
            if len(coords_now) == 6:
                coords = coords_now
            detect.move(real_y, d)
            detect.move_back(d + 100)



