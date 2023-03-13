import cv2
import numpy as np
import imutils

# cv2.namedWindow("preview")
cap = cv2.VideoCapture(0)
low_red = (17, 50, 110)
high_red = (101, 140, 180)
high_green = (185,255,87)
low_green = (80,132,20)
i = 0
img_orig=None
while True:
    try:
        success, img_orig = cap.read()
        img=img_orig.copy()
        img = cv2.inRange(img, low_green, high_green)
        img=cv2.Canny(img,150,150)
        kernel=np.ones((13,13),np.uint8)
        img=cv2.dilate(img,kernel,iterations=1)

        #минимальная координата
        MinX=np.nanargmax(img,axis=0)#.min()
        MinX=np.where(MinX!=0)[0].min()
        MinY=np.nanargmax(img,axis=1)#
        MinY = np.where(MinY != 0)[0].min()

        #максимальная координата
        MaxX = np.nanargmax(img[-1::-1], axis=0)  # .min()
        MaxX = np.where(MaxX != 0)[0].max()
        MaxY = np.nanargmax(img[-1::-1], axis=1)  # .min()
        MaxY = 479-np.where(MaxY != 0)[0].min()
        #print(MinX,MinY,MaxX,MaxY)

        #прямоугольник
        img_orig=cv2.rectangle(img_orig,(MinX,MinY),(MaxX,MaxY),(255,0,0),2)

        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
    except ValueError:
        pass
    cv2.imshow("result", img_orig)
