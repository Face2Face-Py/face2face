import cv2
#import cv2.cv as cv
import time
import numpy as np
import pickle

# Parameters to use when opening the webcam.
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

font = cv2.FONT_HERSHEY_SIMPLEX
lower = 0
upper = 1

fisherFace = cv2.face.createFisherFaceRecognizer()

treino=fisherFace.load('training')

#with open ('fishface', 'rb') as training:
#    fishface = pickle.load(training)

while(True):
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
            print(type(fisherFace.predict(cut)))




        cv2.imshow('test', frame)
        cv2.waitKey(100)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
