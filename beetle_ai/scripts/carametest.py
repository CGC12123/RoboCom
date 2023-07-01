import cv2

cap = cv2.VideoCapture(2)
while(1):
    ret, frame = cap.read()
    if frame is not None:
        cv2.imshow("img", frame)
        cv2.waitKey(0)