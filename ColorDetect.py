import cv2 as cv
import numpy as np
from StackImg import stackImages
path="Resources/lambo.PNG"
#creating a new window to help us track the color
def empty(a):
    pass
cv.namedWindow("Trackbar")

cv.resizeWindow('Trackbar',640,240)
cv.createTrackbar("Hue Min","Trackbar",0,179,empty)
cv.createTrackbar("Hue Max","Trackbar",19,179,empty)
cv.createTrackbar("Sat Min","Trackbar",110,255,empty)
cv.createTrackbar("Sat Max","Trackbar",240,255,empty)
cv.createTrackbar("Val Min","Trackbar",153,255,empty)
cv.createTrackbar("Val Max","Trackbar",255,255,empty)
while True:
    img=cv.imread(path)
    imgHsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)
    h_min=cv.getTrackbarPos("Hue Min","Trackbar")
    h_max = cv.getTrackbarPos("Hue Max", "Trackbar")
    s_min = cv.getTrackbarPos("Sat Min", "Trackbar")
    s_max = cv.getTrackbarPos("Sat Max", "Trackbar")
    v_min = cv.getTrackbarPos("Val Min", "Trackbar")
    v_max = cv.getTrackbarPos("Val Max", "Trackbar")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    #Now we create a mask so we can detect certain color    inrange img
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])

    mask=cv.inRange(imgHsv,lower,upper)
    #now we will display the orange in the original image
    #and operation in the new image
    imgResult=cv.bitwise_and(img,img,mask=mask)
    imgStack=stackImages(0.7,([img,imgHsv],[mask,imgResult]))
    cv.imshow("Stacked images",imgStack)
    #cv.imshow("lambo",img)
    #cv.imshow("hsv lambo",imgHsv)
    #cv.imshow("hsv lambo mask", mask    )
    cv.waitKey(1)
cv.waitKey(0)