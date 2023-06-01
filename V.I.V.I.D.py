def main():
    if __name__ == '__main__':
        main()
'''Importing Opencv and numpy module'''
import cv2
import numpy as np
"Setting up frame width,can be variable depending on user "
frameWidth = 640
"Setting up frame height,can be variable depending on user"
frameHeight = 480
"0 id is given to the default camera in system here it is webcam"
cap = cv2.VideoCapture(0)


cap.set(3, frameWidth)

cap.set(4, frameHeight)
"Setting up the brightness with id 10"
cap.set(10,150)

myColors = [[101,133,145,161,255,255],
            [120,68,160,145,255,255],
            [162,80,8,179,255,255],
            [29,32,162,96,105,255]]

"function to assign colour values according to the colour detected in the image(pen)"
"to find this value is to get from the chart of colour with pixel(RGB Color Code Chart) in format of BGR"
myColorValues=[[204,0,0],
               [204,0,102],
               [0,0,204],
               [51,255,153]]

"myPoints an empty list created to add new points in it"

myPoints = []         #[x,y,colorID]


"defined a function to find colour in image"
def findColor(img,myColor,myColorValues):
    "converting normal image to imageHSV"
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    "everytime new point would be initialised"
    newPoints=[]
    "counter to count to know which color we are talking about"
    count=0
    "for loop to cover all colors"
    for color in myColors:
        "finding the lower limit of the colour from the list of myColor where each colour values are detected with help of Color detection module "
        lower = np.array(color[0:3])
        "finding the upper limit of the colour"
        upper = np.array(color[3:])
        "masking the image i.e. defining the range in which the colour is detected"
        mask = cv2.inRange(imgHSV, lower, upper)
        "we will send this mask that we used to detect coolours to contour function to find the position of bounding box around it"
        x,y=getcontours(mask)
        "circle around the tip to indicate the tip"
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        "new points are to be appened whose x and y value are not 0"
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        "for testing purpose to fine tune the hyperparameter to the detect the colours with high precision"
        cv2.imshow(str(color[0]), mask)
        count+=1
    return newPoints

"defined a function to find contours in the image"
def getcontours(img):
    "this function is used to get contours from the canny image the parameters include mode of retrieval which is for now set to be extreme contours at extreme part and approximation to smoothen out"
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    "in case if due to noise area of object is less than a fixed quantity or the object is not detected we initialise the values of x,y,w,h"
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        print(area)
        "Contour index is -1 as we want to draw all Contours with colour blue and thickness as 3"

        "applying checks so that any noise can be remove"
        if area>50:
            "we dont need to draw the contours we just need the tip"
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            "finding perimeter"
            peri=cv2.arcLength(cnt,True)
            print(peri)
            "approximate the corner points of each of the close object"
            approx=cv2.approxPolyDP(cnt,0.1*peri,True)
            print(approx)

            "we will get the the x y w and h coordinates of the bounding box of objects which we will later use to draw bounding box"

            x, y , w, h =cv2.boundingRect(approx)

    "now we want the tip of the color pen instead of centre of the pen "
    return x+w//2,y

"defined the function for drawing"
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        "since x and y are inside point function and colourID is also inside points which will give value off myColorValues"
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)

"displaying it"
while True:
    "breaking the video feed into image frames and then reading it"
    success, img=cap.read()
    "images are stored in webcam and module is reading those images"
    cv2.imshow("Webcam",img)
    imgResult=img.copy()
    newPoints=findColor(img , myColors,myColorValues)
    "checking if we are getting something"
    if len(newPoints)!=0:
        "we are using for loop because we cant use list inside list,breaking list and then feeding points"
        for newP in newPoints:
            "mypoints would be appended and myPoints would send to function draw canvas where it will draw"
            myPoints.append(newP)
    "if my points list is not null then draw points"
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result",imgResult)
    "here the image will be displayed for 1ms if it more than that or if the user pressed w on ite keyboard the feed would be stopped"
    if cv2.waitKey(1) & 0xFF == ord('w'):
        break









