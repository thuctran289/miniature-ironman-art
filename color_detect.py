import cv2
import numpy as np
from drawModule import Controls

class point():
    def __init__(self, x,y):
        self.x = x
        self.y = y


#Start cam stream
cap = cv2.VideoCapture(0)
print cap.get(3)
print cap.get(4)
main_controls = Controls((cap.get(3), cap.get(4)))

while(1):

    #Set 'frame' as the current cam capture
    _, frame = cap.read()

    #Blur the frame
    blurframe = cv2.blur(frame, (50, 50))

    #Define color range in BGR
    lower_BGR = np.array([240, 210, 210])
    upper_BGR = np.array([255, 255, 255])

    # Threshold the image to get only the selected colors
    mask = cv2.inRange(blurframe, lower_BGR, upper_BGR)
    contour_mask = mask
    cv2.imshow('mask', mask)

    #Create a contour around the selected colors
    # ret,thresh = cv2.threshold(frame,127,255,0)
    contours,_ = cv2.findContours(contour_mask, 1, 2)

    #If there is a contour, create a rectangle around it and print location
    if len(contours) > 0:
        cnt = contours[0]
        M = cv2.moments(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x+w/2-5,y+h/2-5), (x+w/2+5, y+h/2+5), (0, 0, 255), 3)
        pointA = point(x+w/2,y+h/2)

        print x+w/2, y+h/2

    #Display the final image
    cv2.imshow('frame', frame)
    #If ESC pressed, quit the program
    if cv2.waitKey(1) & 0xFF == 27:
        break

#Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()
