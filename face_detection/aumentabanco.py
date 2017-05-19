import glob
import os
import cv2
import time

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while (True):
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 1)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		#eyes = eye_cascade.detectMultiScale(roi_gray)
		#for (ex,ey,ew,eh) in eyes:
		#    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		cut = cv2.resize(roi_gray, (350, 350))

	cv2.imshow('test', frame)

	print("fique neutro e clique n")	
	if cv2.waitKey(50) & 0xFF == ord('n'):
		n = sorted(os.listdir("dataset/neutral"), key=lambda t: int(t[:-4]))[-1]
		nome = int(n[:-4])+1
		print(n, nome)
		cv2.imwrite("dataset/neutral/%d.jpg" %nome, cut)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()