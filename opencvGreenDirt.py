import cv2
import numpy as np
import imutils

class ColorDetect:
    def __init__(self,lowColor,highColor):
        self.lowColor=lowColor
        self.highColor=highColor
        self.cap = cv2.VideoCapture("C:/Users/pavel/PycharmProjects/OpencvpartG/video_2023-03-18_18-33-59.mp4")
        #self.cap = cv2.VideoCapture(0)

    def Level1(self):
            success, self.img_orig = self.cap.read()
            self.img=self.img_orig.copy()
            self.img = cv2.inRange(self.img, self.lowColor,self.highColor)
            self.img=cv2.Canny(self.img,150,50)
            kernel=np.ones((16,16),np.uint8)
            self.img=cv2.dilate(self.img,kernel,iterations=2)
            return self.img,self.img_orig
class  ColorDirtDetect(ColorDetect):

    def __init__(self, lowColor, highColor):
        super().__init__(lowColor, highColor)
    def DetectDirt(self):
        self.img, self.img_orig = super().Level1()
        try:
            # минимальная координата
            MinX = np.nanargmax(self.img, axis=0)  # .min()
            MinX = np.where(MinX != 0)[0].min()
            MinY = np.nanargmax(self.img, axis=1)  #
            MinY = np.where(MinY != 0)[0].min()
            # максимальная координата
            MaxX = np.nanargmax(self.img[-1::-1], axis=0)  # .min()
            MaxX = np.where(MaxX != 0)[0].max()
            MaxY = np.nanargmax(self.img[-1::-1], axis=1)  # .min()
            MaxY = self.img.shape[0] - np.where(MaxY != 0)[0].min()
            #print('shape= ',self.img.shape)
            #print(MinX,MinY,MaxX,MaxY)
            # прямоугольник
            #self.img_orig = cv2.rectangle(self.img_orig, (MinX, MinY), (MaxX, MaxY), (255, 0, 0), 2)
            #self.img= cv2.rectangle(self.img, (MinX, MinY), (MaxX, MaxY), (255, 0, 0), 2)
        except:
            pass
        return self.img_orig,MinX, MinY, MaxX, MaxY


blue=ColorDirtDetect((218,130,3), (2527,159,45))
red=ColorDirtDetect((133,69,193),(205,127,245))
#green=ColorDirtDetect((80,132,20), (185,255,87))
while cv2.waitKey(100):
    img,bMinX, bMinY, bMaxX, bMaxY =blue.DetectDirt()
    _,rMinX, rMinY, rMaxX, rMaxY=red.DetectDirt()
    #img=green.DetectDirt()
    img = cv2.rectangle(img, (bMinX, bMinY), (bMaxX, bMaxY), (0, 255, 0), 2)
    img = cv2.rectangle(img, (rMinX, rMinY), (rMaxX, rMaxY), (255, 0, 0), 2)
    cv2.imshow("result", img)
    #cv2.imshow("result", imgr)
#xr,yr=red.detect()
