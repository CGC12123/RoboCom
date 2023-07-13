import cv2
import os

# os.system("killall -9  python")
cap = cv2.VideoCapture(2)
# while 1:
_, frame = cap.read()
cv2.imwrite("1.jpg", frame)
# cv2.imshow("img", frame)
# cv2.waitKey(1)