import cv2
import random
from paho.mqtt import client as mqtt_client
import numpy as np
import imutils
import time
import datetime

class ColorDetect:
    def __init__(self,lowColor,highColor):
        self.lowColor=lowColor
        self.highColor=highColor
        self.cap = cv2.VideoCapture(0)
        #self.cap = cv2.VideoCapture(0)

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

blue=ColorDirtDetect((218,130,3), (2527,159,45))
red=ColorDirtDetect((133,69,193),(205,127,245))
green=ColorDirtDetect((80,132,20), (185,255,87))
MPub=MQTT_pub(red,green,blue)
MPub.run()
while cv2.waitKey(100):
        MinX, MinY, MaxX, MaxY=0,0,0,0
        img=blue.DetectDirt()
        _=red.DetectDirt()
        _=green.DetectDirt()
        #print(MinX, gMinY, gMaxX, gMaxY)
        try:
            #img = cv2.rectangle(img, (blue.MinX, blue.MinY), (blue.MaxX, blue.MaxY), (0, 255, 0), 2)
            #img = cv2.rectangle(img, (red.MinX, red.MinY), (red.MaxX, red.MaxY), (255, 0, 0), 2)
            img = cv2.rectangle(img,(green.MinX, green.MinY), (green.MaxX, green.MaxY), (0, 0, 255), 2)
            MPub.publish()
        except cv2.error:
            print("cv2.error")
        cv2.imshow("result", img)
        #cv2.imshow("result", imgr)
    #xr,yr=red.detect()
