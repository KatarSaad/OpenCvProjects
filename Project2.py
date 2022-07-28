import cv2 as cv
import numpy as np
from StackImg import stackImages

##############################
widthImg=640
heightImg=400


##############################

cap = cv.VideoCapture(0)
cap.set(3, widthImg)
cap.set(4, heightImg)
cap.set(10,150)
def getContours(img):
    biggest=np.array([])
    maxArea=0
    contours,hierarchy=cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv.contourArea(cnt)
        #print(area)
        if area>5000:
            #cv.drawContours(imgContour,cnt,-1,(255,0,0),3)#-1 draw all contours
            peri=cv.arcLength(cnt,True)
            #print(peri)
            approx=cv.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))###approximate the corner points/predicting the shapes  in the image
            objCor=len(approx)
            if area >maxArea and objCor==4:
                biggest =approx
                maxArea=area

            x,y,w,h=cv.boundingRect(approx)
            #cv.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)

            #cv.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv.drawContours(imgContour,biggest, -1, (255, 0, 0),3)  # -1 draw all contours

    return biggest

#####################################


def preProcessing(img)  :
    imgGray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    imgBlur =cv.GaussianBlur(imgGray,(5,5),1)
    imgCanny=cv.Canny(imgBlur,200,200)

    kernel=np.ones((5,5))
    imgDial=cv.dilate(imgCanny,kernel=kernel,iterations=2)
    imgThresh=cv.erode(imgDial,kernel,iterations=1)
    return imgThresh
#############################################
def getwarp(img,biggest):
    print(biggest)
    biggest=reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv.warpPerspective(img, matrix, (widthImg, heightImg))
    imgCroped=imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCroped=cv.resize(imgCroped,(widthImg,heightImg))


    return imgCroped
###############################
def reorder (myPoints):
    myPoints=myPoints.reshape((4,2))
    myPointsNew=np.zeros((4,1,2),np.int32)
    add=myPoints.sum(1)
    #print("add",add)#axes 1
    myPointsNew[0]=myPoints[np.argmin(add)]
    myPointsNew[3]=myPoints[np.argmax(add)]
    diff=np.diff(myPoints,axis=1)
    myPointsNew[1]=myPoints[np.argmin(diff)]

    myPointsNew[2]=myPoints[np.argmax(diff)]
    #print("new Points ",myPointsNew)
    return myPointsNew
while True:
    success, img = cap.read()
    #img=cv.imread("Resources/paper.jpg")
    cv.resize(img,(widthImg,heightImg))
    imgContour=img.copy()

    imgThreash=preProcessing(img)
    biggest=getContours(imgThreash)
    #getwarp(img,biggest)
    print(biggest)
    if biggest.size !=0:

        imgWarper=getwarp(img,biggest)
        imgArray = ([img, imgContour], [imgThreash, imgWarper])
        #cv.imshow("img warped",imgWarper)
    else :imgArray = ([img, imgContour], [imgThreash, img])



    stackedImages=stackImages(0.8,imgArray)
    cv.imshow("All images with wraped too",stackedImages)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
