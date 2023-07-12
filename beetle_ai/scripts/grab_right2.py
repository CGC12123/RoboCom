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
        rospy.init_node('grab_right', anonymous=True)
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
    # 单点进程 竖直方向初次夹取
    def move_high(self, x, y, dist):
        global done
        time.sleep(0.2)
        # 抓取
        # 对位置并抬高
        coords_ori = grabParams.coords_right_high
        coords_target = [coords_ori[0] + x,  coords_ori[1],  coords_ori[2] + 30, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target, 70, 0)
        time.sleep(0.5)
        # 为了防止卡死先对位置
        coords_target_2 = [coords_ori[0] + grabParams.bias_right_high_x + x,  coords_ori[1],  
                           coords_ori[2] + grabParams.bias_right_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target_2, 70, 0)
        time.sleep(0.2)
        # 移动到目标位置
        coords_target_3 = [coords_ori[0] + grabParams.bias_right_high_x + x,  coords_ori[1] + grabParams.bias_right_high_y,  
                           coords_ori[2] + grabParams.bias_right_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
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
        coords_ori = grabParams.coords_right_low
        # 对位置
        coords_target = [coords_ori[0] + grabParams.bias_right_low_x + x,  coords_ori[1], coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target, 70, 0)
        time.sleep(0.6)
        coords_target1 = [coords_ori[0] + grabParams.bias_right_low_x + x,  coords_ori[1] + grabParams.bias_right_low_y,  
                         coords_ori[2] + grabParams.bias_right_low_z, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target1, 70, 0)
        time.sleep(0.6)
        # 夹取
        basic.grap(True)
        time.sleep(0.5)
        # 退出前抬高
        coords_target_2 = [coords_ori[0] + grabParams.bias_right_low_x + x,  coords_ori[1] + grabParams.bias_right_low_y + 35,  
                           coords_ori[2] + grabParams.bias_right_low_z+15, coords_ori[3], coords_ori[4], coords_ori[5]]
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
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))

        return frame

    #图像处理，适配物体识别
    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))

        return frame

    def obj_detect(self, img):
        x=y=0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        right_target = 0
        net = cv2.dnn.readNetFromONNX(grabParams.ONNX_MODEL)
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (grabParams.IMG_SIZE, grabParams.IMG_SIZE), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)

        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
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
                cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), 2)
                cv2.imwrite('../img/obj/target.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])
            else:
                done = True
                self.mc.set_color(255,192,203) #识别不到，亮粉灯
                return None


        # Print time (inference-only)
        # print("time: " + str(t2-t1) + "s")  

      
        if x+y > 0:
            return x, y
        else:
            return None
        
    def check_position(self, img):
        x = y = 0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        rightmost_box = None
        rightmost_x = 0
        net = cv2.dnn.readNetFromONNX(grabParams.ONNX_MODEL)
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (grabParams.IMG_SIZE, grabParams.IMG_SIZE), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)

        if boxes is not None:
            for i in range(len(classes)):
                # if classes[i] == grabParams.detect_target:
                box = boxes[i]
                x = int((box[0] + box[2]) / 2)
                if x > rightmost_x:
                    rightmost_box = box
                    rightmost_x = x

            if rightmost_box is not None:
                left, top, right, bottom = rightmost_box
                x = int((left + right) / 2)
                y = int((top + bottom) / 2)
                w = bottom - top
                h = right - left
                cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), 2)
                cv2.imwrite('../img/obj/target.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])

            else:
                done = True
                self.mc.set_color(255, 192, 203)  # 识别不到，亮粉灯
                return None

        return x, y

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
        f = open("/home/robuster/RoboCom/beetle_ai/scripts/direction.txt", "r+")
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
        if go_count >= 0:
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
        else:
            while True:
                move_cmd.linear.x = -0.1
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
    os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right.py --debug") # 回到初始状态 
    detect = Detect_marker()
    # detect.run()
    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5) 
    # 调整位置
    x = 0
    y = 0
    frame = cap.read()
    result = detect.check_position(frame)
    while result is None:
        detect.going(2) # 往前走一段继续识别
        frame = cap.read()
        result = detect.check_position(frame)
    
    detect.going(detect.c_x - result[0]) # 尽量对准第一个

    # 开始夹取
    for i in range(0, 5):
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
            # print("move")
            detect.mc.set_color(255,0,0) #抓取开始，亮红灯

            detect.move_high(real_x, real_y, 0)
            # detect.going(20) # 往前到下一个抓取位置

        os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right_low.py --debug")
        detect = Detect_marker()
        # detect.run()
        # cap = FastVideoCapture(grabParams.cap_num)
        # time.sleep(0.5) 
        time.sleep(1) # 等待到达位置
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
            # print("move")
            detect.move_low(real_x, real_y, 0)
        os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right.py --debug") # 回到初始状态 

        if i is not 4:
            detect.going(10) # 往前到下一个抓取位置
        else:
            os.system("python /home/robuster/RoboCom/navigation/BackNavigation.py")

def going_test():
    detect = Detect_marker()
    detect.going(3)
            
if __name__ == "__main__":
    main()
    # going_test()