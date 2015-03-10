import cv2
import numpy as np
import time

class Point():
    def __init__(self, x,y):
        self.x = x
        self.y = y

class Light():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class ColorBox():
    def __init__(self, x, y, w, h, r, g, b):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.g = g
        self.b = b

pointer = Point(0, 0)
light = Light(0, 0, 0, 0)
box = ColorBox(10, 430, 100, 100, 0, 0, 0)

#Start cam stream
cap = cv2.VideoCapture(0)

#Positions list
points = []

while(1):
    #Set 'frame' as the current cam capture
    _, frame = cap.read()

    #Flip the frame over the vertical axis (so that it looks like looking into a mirror)
    frame = cv2.flip(frame, 1)

    #Find the average color of the ColorBox
    colorSegment = frame[box.y : box.y+box.h, box.x : box.x+box.w]
    b,g,r = cv2.split(colorSegment)
    box.b = np.average(b)
    box.g = np.average(g)
    box.r = np.average(r)

    #Outline the ColorBox
    cv2.rectangle(frame, (box.x, box.y), (box.x+box.w, box.y+box.h), (0, 0, 255), 1)

    #Display the current drawing color
    cv2.circle(frame, (100, 100), 50, (box.b, box.g, box.r), -1)

    #Blur the frame
    blurframe = cv2.blur(frame, (50, 50))

    #Define color range in BGR
    lower_BGR = np.array([210, 150, 150])
    upper_BGR = np.array([255, 255, 255])

    # Threshold the image to get only the selected colors
    mask = cv2.inRange(blurframe, lower_BGR, upper_BGR)
    contour_mask = mask
    cv2.imshow('mask', mask)

    #Create a contour around the selected colors
    contours,_ = cv2.findContours(contour_mask, 1, 2)

    #If there is a contour, add the position and current drawing color to a list
    if len(contours) > 0:
        cnt = contours[0]
        M = cv2.moments(cnt)

        #Define the color-tracked light source
        light.x, light.y, light.w, light.h = cv2.boundingRect(cnt)

        #Assign the position of the pointer
        pointer.x = light.x
        pointer.y = light.y

        #Add the pointer and color characteristics to a reference list
        points.append([[pointer.x+light.w/2, pointer.y+light.h/2], [box.b, box.g, box.r]])

    #If there is anything to be drawn, draw it!
    if len(points) > 0:
        for i in xrange(len(points)):
            cv2.circle(frame, (points[i][0][0], points[i][0][1]), 5, (points[i][1][0], points[i][1][1], points[i][1][2]), -1)

    #Display the final image
    cv2.imshow('frame', frame)
    #If ESC pressed, quit the program
    if cv2.waitKey(1) & 0xFF == 27:
        break

#Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()