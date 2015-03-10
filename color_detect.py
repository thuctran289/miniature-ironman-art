import cv2
import numpy as np
import time
from drawModule import Controls

class point():
    def __init__(self, x,y):
        self.x = x
        self.y = y


#Start cam stream
cap = cv2.VideoCapture(0)

points = []

while(1):
    #Set 'frame' as the current cam capture
    _, frame = cap.read()

    #Flip the frame over the vertical axis (so that it looks like looking into a mirror)
    frame = cv2.flip(frame, 1)

    #Find the average color of a segment of the screen
    colorSegment = frame[430:530, 10:110]
    b,g,r = cv2.split(colorSegment)
    avgB = np.average(b)
    avgG = np.average(g)
    avgR = np.average(r)

    #Outline the color-selecting box
    cv2.rectangle(frame, (10, 430), (110, 530), (0, 0, 255), 1)

    #Display the current drawing color
    cv2.circle(frame, (100, 100), 50, (avgB, avgG, avgR), -1)

    #Blur the frame
    blurframe = cv2.blur(frame, (50, 50))

    #Define color range in BGR
    lower_BGR = np.array([230, 210, 210])
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
        x,y,w,h = cv2.boundingRect(cnt)
        points.append([[x+w/2, y+h/2], [avgB, avgG, avgR]])

    #If there is anything to be drawn, draw it!
    if len(points) > 0:
        for i in xrange(len(points)):
            cv2.circle(frame, (points[i][0][0], points[i][0][1]), 3, (points[i][1][0], points[i][1][1], points[i][1][2]), -1)

    #Display the final image
    cv2.imshow('frame', frame)
    #If ESC pressed, quit the program
    if cv2.waitKey(1) & 0xFF == 27:
        break

#Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()