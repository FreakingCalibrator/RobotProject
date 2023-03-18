'''import cv2
import numpy as np
#import imutils

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
    cv2.imshow("result", img_orig)'''

import cv2
import numpy as np
import imutils

class ColorDetect:
    def __init__(self,lowColor,highColor):
        self.lowColor=low_red
        self.highColor=high_red
        cap = cv2.VideoCapture(0)

    def Level1(self):
            success, img_orig = cap.read()
            img=img_orig.copy()
            img = cv2.inRange(img, self.highColor,self.lowColor)
            img=cv2.Canny(img,50,150)
            kernel=np.ones((13,13),np.uint8)
            img=cv2.dilate(img,kernel,iterations=2)
            return img,img_orig
class DetectDirt(ColorDetect):
    def DetectDirt(self):
        try:
            cont=cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cont=imutils.grab_contours(cont)
            cont=sorted(cont,key=cv2.contourArea,reverse=True)[:2]
            pos=None
            ymin =None
            for c in cont:
                    approx=cv2.approxPolyDP(c,19,True)
                    if len(approx)==4:
                        pos=approx
                        break
                    # минимальные значения
            try:
                xmax,ymax,xmin,ymin=[],[],[],[]
                xmax=max([pos[i][0][0] for i in range(0,4)])#.max()
                        #xmax=pos[:][0][0].shape#.max()
                        #print(xmax)
                ymax = max([pos[i][0][1] for i in range(0, 4)])#.max()
                xmin=min([pos[i][0][0] for i in range(0, 4)])#.min()
                ymin = min([pos[i][0][1] for i in range(0, 4)])#.min()
                img_orig=cv2.rectangle(img_orig,(xmin,ymin),(xmax,ymax),(0,0,255),2)
            except:
                pass
            cv2.imshow("result", img_orig)
        except ValueError:
            pass
        return (xmin,ymin),(xmax,ymax)
red=ColorTransportDetect((59, 0, 255),(114, 0, 255))
xr,yr=red.detect()
