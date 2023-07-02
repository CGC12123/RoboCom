#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from geometry_msgs.msg import Twist
from pymycobot.mycobot import MyCobot
# from opencv_yolo import yolo
from VideoCapture2 import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse
import pytesseract

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="False")
args = parser.parse_args()

done = grabParams.done

class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()
        rospy.init_node('grab_left', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10) # 10hz
        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on() 
        self.c_x, self.c_y = grabParams.IMG_SIZE/2, grabParams.IMG_SIZE/2
        self.ratio = grabParams.ratio
        self.lv = 940
        self.hr = 2.1
        self.detect_count = 0
        self.clazz = []
        self.direction = 0 
        self.aruco_count = 0

    # Grasping motion
    # 单点进程 竖直方向初次夹取
    def move_high(self, x, y, dist):
        global done
        time.sleep(0.2)
        # 抓取
        # 对位置并抬高
        coords_ori = grabParams.coords_left_high
        coords_target = [coords_ori[0] + x,  coords_ori[1],  coords_ori[2] + 30, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target, 70, 0)
        time.sleep(0.5)
        # 为了防止卡死先对位置
        coords_target_2 = [coords_ori[0] + grabParams.bias_left_high_x + x,  coords_ori[1],  
                           coords_ori[2] + grabParams.bias_left_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target_2, 70, 0)
        time.sleep(0.2)
        # 移动到目标位置
        coords_target_3 = [coords_ori[0] + grabParams.bias_left_high_x + x,  coords_ori[1] + grabParams.bias_left_high_y,  
                           coords_ori[2] + grabParams.bias_left_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target_3, 70, 0)
        time.sleep(0.6)
        basic.grap(True)
        time.sleep(1)

        # 放回
        self.mc.send_coords(grabParams.coords_pitchdown1, 70, 0) # 先抬高
        time.sleep(0.5)
        self.mc.send_coords(grabParams.coords_pitchdown2, 70, 0)
        time.sleep(1)
        basic.grap(False)
        done = True
        time.sleep(1)

        self.mc.set_color(0,255,0) #抓取结束，亮绿灯

    def move_low(self, x, y, dist):
        
        # 以下为夹取下层
        # 抓取
        coords_ori = grabParams.coords_left_low
        # 对位置
        coords_target = [coords_ori[0] + grabParams.bias_left_low_x + x,  coords_ori[1], coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target, 70, 0)
        time.sleep(0.6)
        coords_target1 = [coords_ori[0] + grabParams.bias_left_low_x + x,  coords_ori[1] + grabParams.bias_left_low_y,  
                         coords_ori[2] + grabParams.bias_left_low_z, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target1, 70, 0)
        time.sleep(0.6)
        # 夹取
        basic.grap(True)
        time.sleep(0.5)
        # 退出前抬高
        coords_target_2 = [coords_ori[0] + grabParams.bias_left_low_x + x,  coords_ori[1] + grabParams.bias_left_low_y + 35,  
                           coords_ori[2] + grabParams.bias_left_low_z+15, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target_2, 70, 0)
        time.sleep(0.2)

        # 放回
        self.mc.send_coords(grabParams.coords_pitchdown3, 70, 0) # 先抬高
        time.sleep(0.5)
        self.mc.send_coords(grabParams.coords_pitchdown4, 70, 0)
        time.sleep(1)
        basic.grap(False)
        done = True
        time.sleep(1)
        
        self.mc.set_color(0,255,0) #抓取结束，亮绿灯

    def get_position(self, x, y):
        wx = (self.c_x - x) * self.ratio
        wy = (y - self.c_y) * self.ratio
        return wx, wy
            
    def transform_frame(self, frame):
        frame = cv2.resize(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame


    def obj_detect(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # tesseract_cmd = '/usr/bin/tesseract'
        # boxes = pytesseract.image_to_boxes(img_gray)

        # 指定 Tesseract OCR 引擎的可执行文件路径
        sseract_cmd = '/usr/bin/tesseract'

        # 读取图片
        img = Image.open('test.png')

        # 执行 OCR
        text = pytesseract.image_to_string(img, config='-psm 6', lang='eng', boxes=False, exe=tesseract_cmd)

        # 输出识别结果
        print("OCR Result: %s" % text)

        for box in boxes.splitlines():
            # print(box)
            box = box.split(' ')
            if box[0] == grabParams.character[0] or box[0] == grabParams.characters[character]:
                x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
                cv2.rectangle(img, (x, 640 - y), (w, 480 - h), (0, 0, 255), 2)
                cv2.imwrite("character_detect", img)

                target_x = (x + w)/2
                target_y = (640 + 480)/2
                return target_x, target_y
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
        # 单位为cm
        # if self.direction:
        # go_count = int(dist + grabParams.move_power_high_left + 0.5)
        # else:
        # go_count = int(dist + grabParams.move_power_high_right + 0.5)
        go_count = int(dist * grabParams.dist_bias)
        count = 0
        move_cmd = Twist()
        time.sleep(0.5)
        while True:
            move_cmd.linear.x = 0.1
            move_cmd.angular.z = 0
            if go_count - count < 2:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = 0
            self.pub.publish(move_cmd)
            count += 1
            if count >= go_count:
                break
            self.rate.sleep()
        # 当循环结束时，手动停止机器人运动
        move_cmd.linear.x = 0
        move_cmd.angular.z = 0
        self.pub.publish(move_cmd)

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
    # detect.run()
    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5) 
    frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) # 顺时针转九十度
    frame = detect.transform_frame(frame)
    detect_result = detect.obj_detect(frame)
    if detect_result is None:  
        pass         
    else:   
        x, y = detect_result
        print(x, y)
        real_x, real_y = detect.get_position(x, y)
        detect.move_high(real_x, real_y, 0)
        # detect.going(10) # 往前到下一个抓取位置
            
if __name__ == "__main__":
    main()