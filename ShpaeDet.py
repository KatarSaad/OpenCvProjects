import cv2 as cv
from StackImg import stackImages
import numpy as np
def getContours(img):
    contours,hierarchy=cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv.contourArea(cnt)
        print(area)
        if area>5000:
            cv.drawContours(imgContour,cnt,-1,(255,0,0),3)#-1 draw all contours
            peri=cv.arcLength(cnt,True)
            print(peri)
            approx=cv.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))###approximate the corner points/predicting the shapes  in the image
            objCor=len(approx)

            x,y,w,h=cv.boundingRect(approx)
            cv.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            ##Guessing the shapes
            if objCor==3:
                objectType="tri"
            elif objCor==4:
                if w//h>=0.9 and w//h<=1.1:
                    objectType="Square"
                else :
                    objectType="Rectangle"
            elif objCor>4:
                objectType="Cercle"


            else :objectType="NONE"
            cv.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(imgContour,objectType,
                            (x+(w//2)-10,y+(h//2)-10),cv.FONT_ITALIC,0.8,((0,0,0)))

#####################################

img=cv.imread("Resources/shapes.png")
imgContour=img.copy()
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
imgBlur=cv.GaussianBlur(gray,(7,7),1)

imgBlank=np.zeros_like(img)
imgCanny=cv.Canny(imgBlur,50,50)#threashhold
getContours(imgCanny)
imgStack=stackImages(0.6,([img,gray,imgBlur],
                          [imgCanny,imgContour,imgBlank]))
cv.imshow("Stacked images",imgStack)

#cv.imshow("original",img)
#cv.imshow("gray",gray)
#cv.imshow("Blur",imgBlur)
cv.waitKey(0)



#### geting the contoues
