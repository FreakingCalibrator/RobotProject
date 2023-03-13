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
while True:
    try:
        success, img_orig = cap.read()
        img=img_orig.copy()
        img = cv2.inRange(img, low_green, high_green)
        img=cv2.Canny(img,50,150)
        kernel=np.ones((13,13),np.uint8)
        img=cv2.dilate(img,kernel,iterations=2)

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
           # print(pos)

        # pass
        # print(minmin[0],minmin[1])
        # if maxmax.shape!=0:
        # print(maxmax[0],maxmax[1])

        # print(np.where(np.argmax(img, axis=1),np.argmax(img, axis=1)>0))
        # print(min(np.argmax(img, axis=1)), min(np.argmax(img, axis=0)))
        # print(max(np.argmax(img, axis=1)), max(np.argmax(img, axis=0)))
        cv2.imshow("result", img_orig)
        # =[1,2,3,1]
        # print(l[-1::-1])
        # i+=1
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
    except ValueError:
        pass
