from VideoCapture import FastVideoCapture
import cv2 as cv
import math

if __name__ == "__main__":
    cap_num = 2
    cap = FastVideoCapture(cap_num)
    while cv.waitKey(1)<0:
        image = cap.read()
        cv.imshow("", image)

        # height, width = image.shape[:2]
        # center = (width/2, height/2)
        # rotate_matrix = cv.getRotationMatrix2D(center=center, angle=-90, scale=1)
        # rotated_image = cv.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))
        # cv.imshow("", rotated_image)


        # rows,cols  = image.shape[:2]
        # angle=-90
        # center = ( cols/2,rows/2)
        # heightNew=int(cols*abs(math.sin(math.radians(angle)))+rows*abs(math.cos(math.radians(angle))))
        # widthNew=int(rows*abs(math.sin(math.radians(angle)))+cols*abs(math.cos(math.radians(angle))))

        
        # M = cv.getRotationMatrix2D(center,angle,1)
        # # print(M)
        # M[0,2] +=(widthNew-cols)/2  
        # M[1,2] +=(heightNew-rows)/2 
        # # print(M)

        # rotated_image  = cv.warpAffine(image,M,(widthNew,heightNew))
        # cv.imshow("", rotated_image)
