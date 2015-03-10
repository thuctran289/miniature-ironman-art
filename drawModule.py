import cv2 
import numpy as np
import math 
from matplotlib import pyplot as plt



class point():
    def __init__(self, x,y):
        self.x = x
        self.y = y


class Controls(object):
	def __init__(self, size = (200,200)):
		self.pointer = point(0,0)
		self.rgb = [0,0,0]
		self.circle_radius = 1
		self.screen = np.zeros((size[0],size[1],3),np.uint8)
		self.screen.fill(256)
		self.line = False
		self.line_radius = 1
		self.rectangle = False
		self.radius_plus = False
		self.radius_minus = False
		self.stored_x = screen.shape[0] + 1
		self.stored_y = screen.shape[1] + 1

	def process_points(self, point, tasks, rgb):
		"""
		given some list of things to do... changes pointers point, and 
		resets booleans based on given points.
		
		"""
		self.x = point[0]
		self.y = point[1]
		self.rgb = rgb
		for x in range(0,len(tasks)):
			new_task = tasks[x]
			if new_task == 0 : 
				#DRAW CIRCLE
				cv2.circle(self.screen, (self.x,self.y), self.circle_radius,self.rgb,-1)
			elif new_task == 1:
				#DRAW LINE
				if self.line == False:
					self.line = True
					self.stored_y = self.y
					self.stored_x = self.x
				else:
					self.line = False
					cv2.line(self.screen, (self.stored_x,self.stored_y),(self.x,self.y), self.rgb, self.line_radius)
			elif new_task == 2:
				#DRAW RECTANGLE
				pass
				#cv2.rectangle(self.screen, (self.stored_x,self.stored_y),(self.x,self.y), self.rgb, self.line_radius)
			elif new_task ==3:			
				#ADD TO RADIUS
				self.circle_radius +=1
			elif new_task ==4:
				#SUBTRACT TO RADIUS
				self.line_radius -=1
			elif new_task ==5:
				self.reset()

	def reset(self): 
		self.circle = False
		self.line = False
		self.rectangle = False
		self.radius_plus = False
		self.radius_minus = False

	def draw_to_screen(self, new_screen):
		for x in range(0, self.screen[0]):
			for y in range(0,self.screen[1]):
				for rgb in range(0,3):
					if self.screen[x][y][rgb] == 256:
						pass
					else:
						new_screen[x][y][rgb] = self.screen[x][y][rgb]


def test():
	img = np.zeros((400,400,3),np.uint8)
	img1 = np.copy(img)


	plt.subplot(121),plt.imshow(img),plt.title('Original')
	plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(img1),plt.title('Other')
	plt.xticks([]), plt.yticks([])
	plt.show()
