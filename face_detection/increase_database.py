import glob
import os
import cv2
import time

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
print("aperte 'n' para neutro, 't' para triste, 'h' para feliz, 'a' para bravo e 's' para surpreso")

id = 0

while (True):
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 1)

	rects = []

	for face in faces:
		dici = {}  
		id += 1

		x,y,w,h = face[0],face[1],face[2],face[3]

		dici['id'] = id
		dici['data'] = [x,y,w,h]

		rects.append(dici)

	biggest = None
	biggest_w = 0

	for i in rects:
		if i['data'][2] > biggest_w:
			biggest = i
			biggest_w = i['data'][2]

	try:

		x = biggest['data'][0]
		y = biggest['data'][1]
		w = biggest['data'][2]
		h = biggest['data'][3]


		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		cut = cv2.resize(roi_gray, (350, 350))

	except:
		pass

	cv2.imshow('test', frame)
	key=cv2.waitKey(50)

	
	if key & 0xFF == ord('n'):
		n = sorted(os.listdir("dataset/neutral"), key=lambda t: int(t[:-4]))[-1]
		nome = int(n[:-4])+1
		print(n, nome)
		cv2.imwrite("dataset/neutral/%d.jpg" %nome, cut)

	if key & 0xFF == ord('t'):
		n = sorted(os.listdir("dataset/sadness"), key=lambda t: int(t[:-4]))[-1]
		nome = int(n[:-4])+1
		print(n, nome)
		cv2.imwrite("dataset/sadness/%d.jpg" %nome, cut)

	if key & 0xFF == ord('h'):
		n = sorted(os.listdir("dataset/happy"), key=lambda t: int(t[:-4]))[-1]
		nome = int(n[:-4])+1
		print(n, nome)
		cv2.imwrite("dataset/happy/%d.jpg" %nome, cut)

	if key & 0xFF == ord('s'):
		n = sorted(os.listdir("dataset/surprise"), key=lambda t: int(t[:-4]))[-1]
		nome = int(n[:-4])+1
		print(n, nome)
		cv2.imwrite("dataset/surprise/%d.jpg" %nome, cut)

	if key & 0xFF == ord('a'):
		n = sorted(os.listdir("dataset/anger"), key=lambda t: int(t[:-4]))[-1]
		nome = int(n[:-4])+1
		print(n, nome)
		cv2.imwrite("dataset/anger/%d.jpg" %nome, cut)

cap.release()
cv2.destroyAllWindows()