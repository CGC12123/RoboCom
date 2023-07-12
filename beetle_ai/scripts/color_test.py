#encoding: UTF-8
import cv2 as cv
import numpy as np

#制作颜色字典
color_dist = { 'blue': {'lower':np.array([93, 145, 122]), 'high':np.array([133,255,255])},
            'red': {'lower':np.array([117, 74, 169]), 'high':np.array([179,255,255])},
            'yellow': {'lower':np.array([15, 141, 204]), 'high':np.array([44,255,255])},
            'green': {'lower':np.array([59, 82, 78]), 'high':np.array([87,150,255])},
            'purple': {'lower':np.array([0, 91, 127]), 'high':np.array([179,255,255])},
            }

# 设置目标颜色
target_corlor = 'red'

cap = cv.VideoCapture(2)# 打开摄像头
# cap.set(3,480)# 视频每一帧的宽
# cap.set(4,320)# 视频每一帧的高
cv.namedWindow('camera', cv.WINDOW_AUTOSIZE)

low = color_dist[target_corlor]['lower']
high = color_dist[target_corlor]['high']

def color_find(image):
    if ret:
        # print("camera already!")
        if frame is not None:
            # print("image is already!")
            image_gaussian = cv.GaussianBlur(frame, (5, 5), 0)     # 高斯滤波
            imgHSV = cv.cvtColor(image_gaussian, cv.COLOR_BGR2HSV) # 转换色彩空间

            kernel = np.ones((5,5),np.uint8)  # 卷积核
            mask = cv.erode(imgHSV, kernel, iterations=2)
            mask = cv.dilate(mask, kernel, iterations=1)
            mask = cv.inRange(mask, low, high)
            cnts = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2] # 检测外轮廓
            try:
                area_max = max(cnts, key = cv.contourArea)
                print("get success!")
                rect = cv.minAreaRect(area_max)     # 绘制每个轮廓的最小外接矩形的方法
                box = cv.boxPoints(rect)            # 获取矩形的四个顶点坐标

                left_point_x = np.min(box[:, 0])
                right_point_x = np.max(box[:, 0])
                top_point_y = np.min(box[:, 1])
                bottom_point_y = np.max(box[:, 1])
                
                mid_point_x = (left_point_x + right_point_x)/2
                mid_point_y = (top_point_y + bottom_point_y)/2

                print("coordinate is (%.2f, %.2f)" %(mid_point_x, mid_point_y))

                cv.drawContours(image, [np.int0(box)], -1, (0, 255, 255), 2)    # 绘制矩形
            except :
                print("get failed")
            
            
            image = cv.flip(image, 1) # 镜像操作
            cv.imshow('camera', image)
            cv.waitKey(1)
        else:
            print("image warning!")
    else:
        print("camera warnign!")

if __name__ == "__main__":
    while cap.isOpened():
        ret, frame = cap.read()
        # 返回两个值，第一个为布尔值，表示接入正常，第二个为每帧的画面
        color_find(frame)
    cap.release()
    cv.waitKey(0)
    cv.destroyAllWindows()