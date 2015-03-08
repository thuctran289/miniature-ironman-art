import cv2
import numpy as np

#Start cam stream
cap = cv2.VideoCapture(0)

while(1):

    #Set 'frame' as the current cam capture
    _, frame = cap.read()

    #Blur the frame
    blurframe = cv2.blur(frame, (50, 50))

    #Define color range in BGR
    lower_BGR = np.array([150, 150, 150])
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
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 3)
        print x, y

    #Display the final image
    cv2.imshow('frame', frame)
    #If ESC pressed, quit the program
    if cv2.waitKey(1) & 0xFF == 27:
        break

#Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    publisher()