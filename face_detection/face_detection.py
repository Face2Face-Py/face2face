#!/usr/bin/python
import cv2
#import cv2.cv as cv
import time
import numpy as np
import pickle

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotion order

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

font = cv2.FONT_HERSHEY_SIMPLEX
lower = 0
upper = 1

fisherFace = cv2.face.createFisherFaceRecognizer()

treino=fisherFace.load('training')

id = 0

while(True):
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
        emotion_name = fisherFace.predict(cut)[0]
        cv2.putText(frame,str(emotions[emotion_name]),(200,100), font, 2,(255,255,255),2, cv2.LINE_AA)
        
    except:
        pass

    cv2.imshow('test', frame)
    cv2.waitKey(100)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
