#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from geometry_msgs.msg import Twist
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="False")
args = parser.parse_args()

done = grabParams.done

class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()
        rospy.init_node('grab_under', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10) # 10hz
        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on() 
        self.yolo = yolo()
        self.c_x, self.c_y = grabParams.IMG_SIZE/2, grabParams.IMG_SIZE/2
        self.ratio = grabParams.ratio
        self.lv = 940
        self.hr = 2.1
        self.detect_count = 0
        self.clazz = []
        self.direction = 0 
        self.aruco_count = 0
        # 颜色字典
        self.color_dist = { 'blue': {'lower':np.array([98, 112, 75]), 'high':np.array([179, 255, 255])},
                            'red': {'lower':np.array([0, 113, 174]), 'high':np.array([13,255,255])}}

    # Grasping motion
    # 单点进程
    def move(self, x, y, dist):
        global done
        self.going(x) # x 的误差使用前后移动来弥补
        time.sleep(0.2)

        # 初步对位置
        coords_ori = grabParams.coords_down
        coords_target = [coords_ori[0],  coords_ori[1]+y,  grabParams.grab_down, coords_ori[3] + grabParams.pitch_down,  coords_ori[4] + grabParams.roll_down,  coords_ori[5] - y/2]
        self.mc.send_coords(coords_target, 70, 0)
        time.sleep(0.2)

        # 移动到抓取的位置 写死
        coords_grab_target = [ ] # 需要先给个预先值 从预先值开始细调 使用误差值_down #########################################################
        self.mc.send_coords(coords_grab_target, 70, 0)
        time.sleep(0.2) # 等待移动到抓取的位置

        # 抓取
        self.mc.set_color(255,0,0)  #抓取，亮红灯
        basic.grap(True)
        time.sleep(0.4)

        # 放回
        time.sleep(0.2)
        self.mc.send_coords(grabParams.coords_pitchdown, 70, 0)
        basic.grap(False) 
        done = True
        self.mc.set_color(0,255,0) #抓取结束，亮绿灯

    def get_position(self, x, y):
        wx = (self.c_x - x) * self.ratio
        wy = (y - self.c_y) * self.ratio
        return wx, wy
            
    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame
   
    # 识别色块
    def obj_detect(self, img, color):
        low = self.color_dist[color]['lower'] # 阈值设置
        high = self.color_dist[color]['high']

        image_gaussian = cv2.GaussianBlur(img, (5, 5), 0)     # 高斯滤波
        imgHSV = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV) # 转换色彩空间

        kernel = np.ones((5,5),np.uint8)  # 卷积核
        mask = cv2.erode(imgHSV, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.inRange(mask, low, high)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] # 检测外轮廓
        try:
            max_contour = max(cnts, key=cv2.contourArea)
            rect = cv2.minAreaRect(max_contour)
            box = cv2.boxPoints(rect)
            cv2.drawContours(img, [np.int0(box)], -1, (0, 255, 255), 2)
            left_point_x = np.min(box[:, 0])
            right_point_x = np.max(box[:, 0])
            top_point_y = np.min(box[:, 1])
            bottom_point_y = np.max(box[:, 1])
            
            mid_point_x = (left_point_x + right_point_x)/2
            mid_point_y = (top_point_y + bottom_point_y)/2
            
            mid_point_x = round(mid_point_x, 2) # 保留两位小数
            mid_point_y = round(mid_point_y, 2)

            # distance = (((mid_point_x - 320) ** 2) + ((mid_point_y - 240) ** 2))**0.5 # 去年的代码 现在不知道干什么用的了

            return mid_point_x, mid_point_y
            
        except :
            return None


    def distance(self, w):
        dist = self.hr / w * self.lv
        dist = dist - 9 - grabParams.set_diff
        return dist

    def aruco(self, frame):
        global done
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        while(1):
            self.aruco_count += 1
            corners, _, _ = cv2.aruco.detectMarkers(
                gray, cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250), parameters=cv2.aruco.DetectorParameters_create()
                )
            if len(corners) > 0:
                x = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
                y = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]
                x = x/4.0
                y = y/4.0
                x_size_p = abs(x - corners[0][0][0][0])*2
                y_size_p = abs(y - corners[0][0][0][1])*2
                lenth = (x_size_p + y_size_p)/2
                dist = self.distance(lenth)
                return dist
            elif self.aruco_count == 3:
                done = True
                self.mc.set_color(255,192,203) #二维码看不到，亮粉灯
                return None

    def run(self):
        self.mc.set_color(0,0,255) #成功调用程序，亮蓝灯
        f = open("/home/robuster/beetle_ai/scripts/direction.txt", "r+")
        self.direction = int(f.read())
        f.seek(0)
        f.truncate()
        f.write('0')
        f.close()

    def going(self, dist):
        if self.direction:
            go_count = int(dist + grabParams.move_power_high_left + 0.5)
        else:
            go_count = int(dist + grabParams.move_power_high_right + 0.5)
        count = 0
        move_cmd = Twist()
        time.sleep(0.5)
        while(1):
            self.pub.publish(move_cmd)
            count += 1
            move_cmd.linear.x = 0.1
            move_cmd.angular.z = 0
            if go_count - count < 2:
                move_cmd.linear.x = 0.05 
                move_cmd.angular.z = 0
            if count == go_count:
                break
            self.rate.sleep()

    def back(self):
        count = 6
        move_cmd = Twist()
        move_cmd.linear.x = -0.3
        if grabParams.put_down_direction == "right":
            move_cmd.angular.z = -0.3
        else:
            move_cmd.angular.z = 0.3
        time.sleep(0.5)
        while(count):
            self.pub.publish(move_cmd)
            count-=1
            self.rate.sleep()

    # 需要修改为新的放置位置
    def put_down(self):
        self.mc.send_coords([15,-192,300,-125,60,152], 70, 0)
        basic.grap(False)

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(500) 
        
def main():
    detect = Detect_marker()
    detect.run()
    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5) 
    for i in range(0, 5):
        frame = cap.read()
        frame = detect.transform_frame(frame)
        detect_result = detect.obj_detect(frame, grabParams.color)
        if detect_result is None:           
            pass
        else:   
            x, y = detect_result
            real_x, real_y = detect.get_position(x, y)
            detect.move(real_x, real_y + grabParams.y_bias, 0)
        detect.going(20) # 往前到下一个抓取位置
            
if __name__ == "__main__":
    main()