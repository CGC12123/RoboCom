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
        rospy.init_node('grab_high', anonymous=True)
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

    # Grasping motion
    def move(self, x, y, dist):
        global done
        if self.direction:
            coords_ori = grabParams.coords_high_left # left
            coords_target = [coords_ori[0],  coords_ori[1]+y,  grabParams.grab_high_left, coords_ori[3] + grabParams.pitch_high_left,  coords_ori[4] + grabParams.roll_high_left,  coords_ori[5] - y/2]
        else:
            coords_ori = grabParams.coords_high_right# right
            coords_target = [coords_ori[0],  coords_ori[1]+y/3,  grabParams.grab_high_right,  coords_ori[3] + grabParams.pitch_high_right,  coords_ori[4] + grabParams.roll_high_right,  coords_ori[5] - y/2]
        self.mc.send_coords(coords_target, 70, 0)
        time.sleep(0.2)
        self.mc.set_color(255,0,0)  #抓取，亮红灯
        self.going(dist) 
        time.sleep(0.2)
        basic.grap(True)
        time.sleep(0.4)
        self.back() 
        time.sleep(0.2)
        self.put_down() 
        done = True
        self.mc.set_color(0,255,0) #抓取结束，亮绿灯

    def get_position(self, x, y):
        wx = (self.c_x - x) * self.ratio
        wy = (y - self.c_y) * self.ratio
        return wx, wy
            
    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame
   
    def obj_detect(self, img):
        global done
        x = y = 0
        w = h = 0
        right_target = 0
        net = cv2.dnn.readNetFromONNX(grabParams.ONNX_MODEL)
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (grabParams.IMG_SIZE, grabParams.IMG_SIZE), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        if boxes is not None:
            for i in range(len(classes)):
                if classes[i] == grabParams.detect_target:
                    self.clazz.append(i)
            if len(self.clazz):
                scores_max = scores[self.clazz[0]]
                right_target = self.clazz[0]
                for i in range(len(self.clazz)):
                    if scores[self.clazz[i]] > scores_max:
                        scores_max = scores[self.clazz[i]]
                        right_target = self.clazz[i]
                self.yolo.draw(img, zip(boxes)[right_target], zip(scores)[right_target], zip(classes)[right_target])
                left, top, right, bottom = boxes[right_target]
                x = int((left+right)/2)
                y = int((top+bottom)/2)
                w = bottom - top
                h = right - left    
            else:
                done = True
                self.mc.set_color(255,192,203) #识别不到，亮粉灯
                return None
        else:
            self.detect_count+=1
            if self.detect_count == 5:
                done = True
                self.mc.set_color(255,192,203) #识别不到，亮粉灯
            return None
        if w > h:
            width = w
        else: 
            width = h
        if x+y > 0:
            return x, y, width
        else:
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

    def put_down(self):
        if grabParams.put_down_direction == "right":
            self.mc.send_coords([15,-192,300,-125,60,152], 70, 0)
        else:
            self.mc.send_coords([17,211,260,-90,35,-35], 70, 0)

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(500) 
        
def main():
    detect = Detect_marker()
    detect.run()
    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5) 
    while cv2.waitKey(1) < 0 and not done:
        frame = cap.read()
        frame = detect.transform_frame(frame)
        detect_result = detect.obj_detect(frame)
        if detect_result is None:           
            continue
        else:   
            dist_aruco = detect.aruco(frame)  
            if dist_aruco != None:       
                x, y, _ = detect_result
                real_x, real_y = detect.get_position(x, y)
                detect.move(0, real_y + grabParams.y_bias, dist_aruco)
            else:
                cap.close()
            
if __name__ == "__main__":
    main()
