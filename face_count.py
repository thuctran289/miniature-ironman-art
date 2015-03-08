def num_faces():
	"""Output a blurred images based on the number of faces in front of the webcam"""

	import cv2
	import numpy as np
	import filterModule

	cap = cv2.VideoCapture(0)
	cap.set(3, 240)
	cap.set(4, 160)

	#face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascades_frontalface_alt.xml')
	#face_cascade = cv2.CascadeClassifier('/home/skelly1/OpenCV/opencv-2.4.10/data/haarcascades/haarcascades_frontalface_alt.xml')
	face_cascade = cv2.CascadeClassifier('/home/skelly1/opencv-2.4.10/data/haarcascades/haarcascade_frontalface_alt.xml')
	# kernel = np.ones((21,21),'uint8')

	while(True):
		ret, frame = cap.read()
		# cap.set(3, 480)
		# cap.set(4, 360)
		# frame = frame[1:500,1:500,::]
		#Create an array of the detected faces
		#faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
		#res = filterModule.filter_by_count(frame, len(faces))
		# res = filterModule.color_filter_by_count(frame, len(faces))

		# if len(faces) == 0:
		# 	mask = cv2.inRange(frame, (0, 0, 0), (255, 150, 150))
		# 	res = cv2.bitwise_and(frame,frame, mask= mask)
		# elif len(faces) == 1:
		# 	mask = cv2.inRange(frame, (0, 0, 0), (255, 150, 255))
		# 	res = cv2.bitwise_and(frame,frame, mask= mask)
		# elif len(faces) == 2:
		# 	res = frame

		# Display the blurred/clear image
		# cv2.imshow('res', res)
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == 27:
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

num_faces()