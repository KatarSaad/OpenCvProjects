import cv2 as cv
import numpy as np
from StackImg import stackImages
count=0
color=(255,0,255)
minArea=500
widthImg=640
heightImg=400
plateCascade = cv.CascadeClassifier("Resources/haarcascade_russian_plate_number.xml")
#############################################
cap = cv.VideoCapture(0)
cap.set(3, widthImg)
cap.set(4, heightImg)
cap.set(10,150)

while True:

    success, img = cap.read()
    img1=cv.imread("Resources/p2.jpg")



    imgGray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

    plates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in plates:

        area=w*h

        if area>minArea:
            cv.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv.putText(img1,"Number Plate",(x,y-5),
                       cv.FONT_HERSHEY_SCRIPT_COMPLEX,1,color,2)
            imgRoi=img1[y:y+h,x:x+w]
            #cv.imshow("Plate detetected  ",imgRoi)



    cv.imshow("Result", img1)

    imgResult=img.copy()
   #cv.imshow("Cam",img)



    if cv.waitKey(1) & 0xFF == ord('s'):
        cv.imwrite("Resources/Scanned/NoPlate "+str(count)+".jpg",imgRoi)
        cv.rectangle(img1,(0,200),(640,300),(0,255,0),cv.FILLED)
        cv.putText(img,"Scanned",(150,265),cv.FONT_HERSHEY_SCRIPT_COMPLEX,2,(0,0,255),2 )
        cv.imshow("Resultz",img)
        cv.waitKey(500)
        count+=1



