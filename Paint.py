import cv2 as cv
import numpy as np
from StackImg import stackImages

myColors = [[5,107,0,19,255,255],
            [133,56,0,159,156,255],
            [57,76,0,100,255,255],
            [90,48,0,118,255,255]]
myColorValues = [[51,153,255],          ## BGR
                 [255,0,255],
                 [0,255,0],
                 [255,0,0]]
myPoints =[]#[x,y,colorID]
newPoints=[]

def drawOnCanvas(myPoints,myColorsValues):
    for point in myPoints:
        cv.circle(imgResult, (point[0], point[1]), 10, myColorsValues[point[2]], cv.FILLED)


def getContours(img):
    contours,hierarchy=cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv.contourArea(cnt)
       # print(area)
        if area>5000:
            #cv.drawContours(imgResult,cnt,-1,(255,0,0),3)#-1 draw all contours
            peri=cv.arcLength(cnt,True)
            #print(peri)
            approx=cv.approxPolyDP(cnt,0.02*peri,True)
            #print(len(approx))###approximate the corner points/predicting the shapes  in the image
            #objCor=len(approx)

            x,y,w,h=cv.boundingRect(approx)
            #print(x,y,w,h)
            #cv.rectangle(imgResult,(x,y),(x+w,y+h),(0,255,0),2)
            ##Guessing the shapes
    return  x+w//2,y




def findColor(img,myColors,myColorsValues):
    imgHsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count=0
    for color in myColors:


        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv.inRange(imgHsv, lower, upper)
        x,y=getContours(mask)
        cv.circle(imgResult,(x,y),10,myColorsValues[count],cv.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        #cv.imshow(str(color[0]),mask)
    return newPoints


frameWidth = 640
frameHeight = 480
cap = cv.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
while True:
    success, img = cap.read()
    imgResult=img.copy()
    newPoints=findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for p in newPoints:
            myPoints.append(p)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv.imshow("Result", imgResult)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


