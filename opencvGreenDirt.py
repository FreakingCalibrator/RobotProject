import cv2
import random
from paho.mqtt import client as mqtt_client
import numpy as np
import imutils
import time
import datetime
import math

class ColorDetect:
    
    def __init__(self,lowColor,highColor):
        self.lowColor=lowColor
        self.highColor=highColor
        #self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture("/home/galahad/programs/python/mqtt/vid-20230401-133905_baADU9Q5.mp4")
        self.cap = cv2.VideoCapture("/home/galahad/programs/python/mqtt/VID_20230401_133905.mp4")
    def Level1(self):
        try:
            success, self.img_orig = self.cap.read()
            self.img=self.img_orig.copy()
            self.img = cv2.inRange(self.img, self.lowColor,self.highColor)
            self.img=cv2.Canny(self.img,150,50)
            kernel=np.ones((16,16),np.uint8)
            self.img=cv2.dilate(self.img,kernel,iterations=2)
            return self.img,self.img_orig
        except AttributeError:
            print("AttributeError")

class  ColorDirtDetect(ColorDetect):
    
    def __init__(self, lowColor, highColor):
        super().__init__(lowColor, highColor)
        self.MinX=0
        self.MinY=0
        self.MaxX=0
        self.MaxY=0
    def DetectDirt(self):
        try:
            self.img, self.img_orig = super().Level1()
        except TypeError:
            print("TypeError")
        try:
            # минимальная координата
            self.MinX = np.nanargmax(self.img, axis=0)  # .min()
            self.MinX = np.where(self.MinX != 0)[0].min()
            self.MinY = np.nanargmax(self.img, axis=1)  #
            self.MinY = np.where(self.MinY != 0)[0].min()
            # максимальная координата
            self.MaxX = np.nanargmax(self.img[-1::-1], axis=0)  # .min()
            self.MaxX = np.where(self.MaxX != 0)[0].max()
            self.MaxY = np.nanargmax(self.img[-1::-1], axis=1)  # .min()
            self.MaxY = self.img.shape[0] - np.where(self.MaxY != 0)[0].min()
            #print('shape= ',self.img.shape)
            #print(MinX,MinY,MaxX,MaxY)
            # прямоугольник
            #self.img_orig = cv2.rectangle(self.img_orig, (MinX, MinY), (MaxX, MaxY), (255, 0, 0), 2)
            #self.img= cv2.rectangle(self.img, (MinX, MinY), (MaxX, MaxY), (255, 0, 0), 2)
        except:
            pass
        return self.img_orig
        #return self.img

class  ColorTransportDetect(ColorDetect):
    
    def __init__(self, lowColor, highColor):
        super().__init__(lowColor, highColor)
        self.MinX=0
        self.MinY=0
        self.MaxX=0
        self.MaxY=0

        self.TrueborderMax=0
        self.TrueborderMin=0

    def DetectTransport(self):
        try:
            self.img, self.img_orig = super().Level1()
        except TypeError:
            print("TypeError")
        try:
            # минимальная координата
            self.MinX = np.nanargmax(self.img, axis=0)  # .min()
            self.MinX = np.where(self.MinX != 0)[0].min()
            self.MinY = np.nanargmax(self.img, axis=1)  #
            self.MinY = np.where(self.MinY != 0)[0].min()
            # максимальная координата
            self.MaxX = np.nanargmax(self.img[-1::-1], axis=0)  # .min()
            self.MaxX = np.where(self.MaxX != 0)[0].max()
            self.MaxY = np.nanargmax(self.img[-1::-1], axis=1)  # .min()
            self.MaxY = self.img.shape[0] - np.where(self.MaxY != 0)[0].min()
            # доп.координаты для линии
            self.TrueborderMax=(np.nanargmax(self.img[self.MinY+1],axis=0),self.MinY)
            #self.img_orig = cv2.circle(self.img_orig, self.TrueborderMax, 20, (244, 0, 0), 1)

            self.TrueborderMin=(np.nanargmax(self.img[self.MaxY-1], axis=0),self.MaxY)
            #self.img_orig=cv2.circle(self.img_orig,self.TrueborderMin,20,(244,0,0),1)

            #print(self.TrueborderMin,self.TrueborderMax)

            # прямоугольник
            #self.img_orig = cv2.rectangle(self.img_orig, (MinX, MinY), (MaxX, MaxY), (255, 0, 0), 2)
            #self.img= cv2.rectangle(self.img, (MinX, MinY), (MaxX, MaxY), (255, 0, 0), 2)
        except:
            pass
        #return self.img_orig
        return self.img

class MQTT_pub:
    def __init__(self,r,g,b):
        self.r=r
        self.g=g
        self.b=b
        self.broker = '192.168.178.27'
        self.port = 1883
        self.topic = "house"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client(self.client_id)
        #client.username_pw_set(username, password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        return self.client


    def publish(self):
        msg_count = 0
        msg = "Xmin:{}; Ymin:{}; Xmax:{}; Ymax:{}".format(self.g.MinX,self.g.MinY,self.g.MaxX,self.g.MaxY) 
        print(msg)
        result = self.client.publish(self.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"'{datetime.datetime.now().strftime('%H:%M:%S')}' > Send `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
        msg_count += 1


    def run(self):
        self.client = self.connect_mqtt()
        self.client.loop_start()
        self.publish()

class Drawing:

    def __init__(self,r,g,b):
        self.red=r
        self.green=g
        self.blue=b
        '''self.MaxXred=0
        self.MinYred=0
        self.MinXblue=0
        self.MinYblue=0'''

    def draw(self,img):
        try:
            img = cv2.rectangle(img, (self.blue.MinX, self.blue.MinY), (self.blue.MaxX, self.blue.MaxY), (0, 255, 0), 2)
            img = cv2.rectangle(img, (self.red.MinX, self.red.MinY), (self.red.MaxX, self.red.MaxY), (255, 0, 0), 2)
            img=cv2.rectangle(img,(self.green.MinX,self.green.MinY),(self.green.MaxX, self.green.MaxY), (0, 0, 255), 2)
            img=cv2.line(img,(self.red.MinX,self.red.MinY),(self.blue.MinX,self.blue.MinY),(255,255,0), 2)
            img=cv2.line(img,(self.red.MaxX,self.red.MaxY),(self.blue.MaxX,self.blue.MaxY),(255,255,0), 2)
            img=cv2.line(img,(self.green.MaxX,self.red.MinX),(self.green.MaxY,self.red.MinY),(0,255,255),2)
            return img
        except:
            pass
    
class Control:
    def __init__(self,r,g,b):
        self.red=r
        self.green=g
        self.blue=b
        self.greenPoint=[10000,10000]
        self.phase=1
        self.point=[self.green.MaxX,self.green.MaxY]
        self.iter=0
    def CalcVector(self):
        ind=None
        try:
            vectorTransport=(self.red.MinX-self.blue.MinX,self.red.MinY-self.blue.MinY)
            lenVectorTransport=math.sqrt(vectorTransport[0]**2+vectorTransport[1]**2)
            vectorTransport=(vectorTransport[0]/lenVectorTransport,vectorTransport[1]/lenVectorTransport)
            #vectorPosition=(self.point[0]-self.red.MinX,self.point[1]-self.red.MinY)
            vectorPosition=(self.point[1]-self.red.MinY,-(self.point[0]-self.red.MinX))
            lenVectorPosition=math.sqrt(vectorPosition[0]**2+vectorPosition[1]**2)
            self.distance=math.sqrt(vectorPosition[0]**2+vectorPosition[1]**2)
            vectorPosition=(vectorPosition[0]/lenVectorPosition,vectorPosition[1]/lenVectorPosition)
            self.angle=np.dot(vectorPosition,vectorTransport)
            if self.distance<10:
                self.point=[self.green.MinX,self.green.MaxY]
                if abs(self.angle)<0.05:
                    self.phase=2

            print(self.phase,self.angle)


        except:
            pass
    def Rotate(self):
        if self.phase==1:
            if self.angle<-0.05:
                print('left')
                #right()
            elif self.angle>0.05:
                print('right')
                #left()
            elif abs(self.angle)<0.05:
                print('go')
                #forward()
        if self.phase==2:
            if self.iter%2==0:
                if abs(self.green.MinX-self.red.MinX)>0.05:
                    print('go')
                    #forward()
                else:
                    print("RightReversal")
                    #RightReversal
            elif self.iter%2!=0:
                if abs(self.green.MaxX-self.red.MaxX)>0.05:
                    print('go')
                    #forward()
                else:
                    print("LeftReversal")
                    #RightReversal

blue=ColorTransportDetect((210,141,0), (226,159,0))
red=ColorTransportDetect((133,69,193),(205,127,245))
green=ColorDirtDetect((104,129,1), (134,149,21))
image=Drawing(red, green,blue)
MPub=MQTT_pub(red,green,blue)
ControlT=Control(red,green,blue)
phase=1
MPub.run()
while cv2.waitKey(250):
        img=blue.DetectTransport()
        img=red.DetectTransport()
        img=green.DetectDirt()
        img=image.draw(img)
        if phase==1:
            ControlT.CalcVector()
        ControlT.Rotate()
        try:
            cv2.imshow("result", img)
        except:
            pass
