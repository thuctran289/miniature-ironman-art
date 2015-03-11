import cv2
import numpy as np
import time
"""
We are using global variables such as frame for this program. 
"""
cap = cv2.VideoCapture(0)
_, frame = cap.read()


class Point():
    def __init__(self, x,y,r):
        self.x = x
        self.y = y
        self.r = r

class Light():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class CommandBox(object):
    """
    Defines a base class for different ways for light to interact with a screen. Defines a box where a command can be activated
    """
    def __init__(self, x, y, w, h,box_bgr):
        """
        Initializes the box's position, size, and color. Will be overwritten in further base classes for more particular roles.
        x,y is lowerleft corner. w,h are width and height, and box_bgr is the color of the box. 
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h 
        self.box_bgr = box_bgr

    def display_box(self):
        """
        This displays to the global frame variable. Just draws the different displays barring other specific requirements. 
        """
        #Uses opencv to write a rectangle to. 
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)

    def inframe(self, point):
        """
        Checks to see if a point is in the frame of the CommandBox.
        """
        #Checks to see if a point is in the range of the box. 
        if self.x<= point.x <= self.x+self.w:
            if self.y<=point.y<=self.y + self.h:
                return True
        else:
            return False

class ColorBox(CommandBox):
    def __init__(self, x, y, w, h, box_bgr, draw_bgr):
        self.draw_bgr = draw_bgr
        super(ColorBox, self).__init__(x,y,w,h,box_bgr)

    def set_draw_color(self, color_segment):
        b,g,r = cv2.split(color_segment)
        self.draw_bgr[0] = np.average(b)
        self.draw_bgr[1] = np.average(g)
        self.draw_bgr[2] = np.average(r)

    def display_box(self):
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.circle(frame, (100, 100), 50, color_box.draw_bgr, -1)


class ResetBox(CommandBox):
    def display_box(self):
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.putText(frame, "R",(self.x,self.y+self.h), cv2.FONT_HERSHEY_SIMPLEX, 2, 0)
    def check_reset(self,pointer, point_array):
        if self.inframe(pointer):
            return []
        else:
            return point_array

class RadiusBox(CommandBox):
    def __init__(self, x, y, w, h,box_bgr,r):
        super(RadiusBox,self).__init__(x,y,w,h,box_bgr)
        self.r = r
    def display_box(self):
        cv2.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.putText(frame, "+",(self.x,self.y+self.h), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.rectangle(frame, (self.x+self.w/2, self.y), (self.x+self.w, self.y+self.h), self.box_bgr, 1)
        cv2.putText(frame, "-",(self.x+self.w/2,self.y+self.h), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    def inframe(self, point):
        if self.x<= point.x <= self.x+self.w/2:
            if self.y<=point.y<=self.y + self.h:
                return 1
        elif self.x+self.w/2<= point.x <= self.x+self.w:
            if self.y<=point.y<=self.y + self.h:
                return -1
        else:
            return 0

    def change_radius(self, pointer):
        if self.inframe(pointer)== 0:
            pass
        elif self.inframe(pointer) ==1:
            self.r += 1
        elif self.inframe(pointer) ==-1:
            self.r -= 1
        if self.r<=1:
            self.r = 1

cap = cv2.VideoCapture(0)
_, frame = cap.read()

pointer = Point(0, 0,5)
light = Light(0, 0, 0, 0)
color_box = ColorBox(0, 430, 100, 100, [0, 0, 255],[0,0,0])
radius_box = RadiusBox(490,430,100,50,[0,255,0],5)
reset_box = ResetBox(590,430,50,50,[255,0,0])
#Start cam stream
#Define color range in BGR
lower_BGR = np.array([210, 150, 150])
upper_BGR = np.array([255, 255, 255])


points = []


while(1):
    #Set 'frame' as the current cam capture
    _, frame = cap.read()
    #Flip the frame over the vertical axis (so that it looks like looking into a mirror)
    frame = cv2.flip(frame, 1)
    #Find the average color of the ColorBox by getting frame of the color, and inputting into function. 
    color_segment = frame[color_box.y : color_box.y+color_box.h, color_box.x : color_box.x+color_box.w]
    color_box.set_draw_color(color_segment)
    #Display the ColorBox Conditions.
    #Blur the frame


    
    #Associated with point detection.
    blurframe = cv2.blur(frame, (50, 50))
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
        pointer.r = radius_box.r
        #Add the pointer and color characteristics to a reference list
        new_color = [color_box.draw_bgr[0],color_box.draw_bgr[1],color_box.draw_bgr[2]]
        points.append([[pointer.x+light.w/2, pointer.y+light.h/2, pointer.r], new_color])
    #If there is anything to be drawn, draw it!

    radius_box.change_radius(pointer)
    points = reset_box.check_reset(pointer, points)

    if len(points) > 0:
        for i in xrange(len(points)):
            cv2.circle(frame, (points[i][0][0], points[i][0][1]), points[i][0][2], (points[i][1][0], points[i][1][1], points[i][1][2]), -1)
    color_box.display_box()
    radius_box.display_box()
    reset_box.display_box()


    #Display the final image
    cv2.imshow('frame', frame)
    #If ESC pressed, quit the program
    if cv2.waitKey(1) & 0xFF == 27:
        break

#Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()