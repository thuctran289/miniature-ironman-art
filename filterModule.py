import cv2
import numpy as np
from matplotlib import pyplot as plt

def filter_by_count(img, number_of_people):
	if (number_of_people ==0):
		kernal = np.ones((80,80),np.float32)/6400
	elif (number_of_people ==1):
		kernal = np.ones((40,40),np.float32)/1600
	elif (number_of_people ==2):
		kernal = np.ones((20,20),np.float32)/400
	elif (number_of_people ==3):
		kernal = np.ones((10,10),np.float32)/100
	elif (number_of_people ==4):
		kernal = np.ones((5,5),np.float32)/25
	else:
		return img
	
	dst = cv2.filter2D(img,-1,kernal)
	return dst
	#plt.subplot(121),plt.imshow(img),plt.title('Original')
	#plt.xticks([]), plt.yticks([])
	#plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
	#plt.xticks([]), plt.yticks([])
	
def color_filter_by_count(img, number_of_people):
	size_of_img = img.shape
	if number_of_people == 0 :
		return np.zeros((size_of_img),np.float32)
	elif (number_of_people ==1):
		for x in range(0,size_of_img[0]):
			for y in range(0,size_of_img[1]):
				img[x,y,0] = 0
				img[x,y,1] = 0

		return img
	elif (number_of_people==2):
		for x in range(0,size_of_img[0]):
			for y in range(0,size_of_img[1]):
				img[x,y,0] = 0

		return img
	else:
		return img
