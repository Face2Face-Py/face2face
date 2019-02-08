#!/usr/bin/env python
__author__      = "Raphael Costa,Bruna Kimura,Frederico Curti,Elisa Malzoni"

import cv2
# import cv2 as cv
import numpy as np
# from matplotlib import pyplot as plt
import time
from PIL import Image
from mss import mss
from chromote import Chromote
import os
import time
import websocket
import json
import platform
import subprocess
import sys
import threading
from loader import Screen
import pickle
import multiprocessing
import leapmotion as lm
import Leap
sys.path.append('./Real-Time-Facial-Expression-Recognition-with-DeepLearning/webcam')
from  webcam_detection import showScreenAndDectect

global reactions

reactions = {}

reactions["happy"] = 0
reactions["surprise"] = 0
reactions["sadness"] = 0
reactions["anger"] = 0
reactions["neutral"] = 0

frameQueue = multiprocessing.Queue()
resultQueue = multiprocessing.Queue()

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def begin():
    # p = multiprocessing.Process(target=showScreenAndDectect, args=(frameQueue, resultQueue))
    # p.start()

    # while True:
    #     f, frame = capture.read()

    #     # frameQueue.put(frame)
    #     # print('waiting...')
    #     # z = resultQueue.get(block=True, timeout=5)
    #     print(exp)

    # p.join()
    
    emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotion order
    osversion = None
    if platform.system() == "Windows":
        osversion = "windows"
        subprocess.Popen('TASKKILL /IM chrome.exe /F')
        time.sleep(2)
        chromedir = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222'
        print 'opening chrome with permissions'
        subprocess.Popen(chromedir)
        print 'chrome open'

    elif platform.system() == "Darwin":
        osversion = "mac"
        os.system("pkill Chrome")
        time.sleep(2)
        os.system('open /Applications/Google\ Chrome.app -n --args --new-window --remote-debugging-port=9222')
    else:
        print "OS not supported"

    
    # If you want to open a video, just change this path
    #cap = cv2.VideoCapture('hall_box_battery.mp4')
    print 'running on ' + osversion
    print 'load remote debugging'
    # Parameters to use when opening the webcam.
    # cap = cv2.VideoCapture(0)
    # cv2.setUseOptimized(True)
    time.sleep(3)
    chrome = Chromote()
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # face_cascade = cv2.CascadeClassifier('face_detection/haarcascade_frontalface_default.xml')
    # fisherFace = cv2.face.FisherFaceRecognizer_create()
    # treino = fisherFace.read('face_detection/training')

    # for i in chrome.tabs:
    #     if chrome.tabs.index(i) != 0:
    #         print "please close all other tabs"
    tab = chrome.tabs[0]
    tab.set_url("https://www.facebook.com/")

    print "waiting 5 secs"
    time.sleep(5)

    # while True:
    #     tab = chrome.tabs[0]
    #     print 'still waiting..'
    #     pagestatus = json.loads(tab.evaluate("document.readyState === 'complete'"))
    #     if pagestatus["result"]["result"]["value"] == True and tab.title == "Facebook":
    #         print "facebook loaded"
    #         break
    #     else:
    #         time.sleep(1)

    print "Please enable JQuery injection and then press OK!"
    tab.evaluate('window.confirm("Please inject jQuery and then press OK");')

    for i in range(3):
        print 3-i
        time.sleep(1)

    print "checking if injection was successful"
    tab.evaluate("console.log('Jquery is ' + typeof jQuery)")

    isloaded = tab.evaluate("typeof jQuery")
    json_string = isloaded
    obj = json.loads(json_string)

    if obj["result"]["result"]["value"] != "function":
        print "JQuery was not injected... Exiting"
        jqueryIsInjected = False
        if osversion == "mac":
            os.system("pkill Chrome")
        elif osversion == "windows":
            subprocess.Popen('TASKKILL /IM chrome.exe /F')
        screen.updateText('There was an error\n when loading JQuery.\n Please try again')
        screen.onScriptStopped()
        raise SystemExit

    try:
        print "trying to inject script"
        with open('script.js', 'r') as content_file:
            content = content_file.read()
            tab.evaluate(content)
    except:
        print "an error ocurred"
        raise SystemExit

    time.sleep(2.5)

    # process = subprocess.Popen(['python3', 'Real-Time-Facial-Expression-Recognition-with-DeepLearning/webcam/webcam_detection.py'], stdout=subprocess.PIPE, bufsize=1)

    print "Functions properly injected!"
    print "Starting leapmotion"
    listener = lm.SampleListener()
    controller = Leap.Controller()
    controller.config.set("background_app_mode", 2)
    controller.config.save()
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    # controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    os.system("open /Applications/Leap\ Motion.app/Contents/MacOS/Visualizer.app")


    jqueryIsInjected = True
    #     tab.evaluate("onPageLoaded();")


    mon = {'top': 160, 'left': 160, 'width':200, 'height': 200}
    sct = mss()


    font = cv2.FONT_HERSHEY_SIMPLEX
    lower = 0
    upper = 1
    id = 0
    swipecooldown = 10
    gesturecooldown = 50

    
    print "Starting face detection"

    valid_reactions = reactions.keys()

    while(jqueryIsInjected == True):
        ret, frame = capture.read()
        exp = showScreenAndDectect(frame)
        if (exp != None and exp in valid_reactions):
            reactions[exp] += 1
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(gray, 1.3, 1)

        # rects = []

        # for face in faces:
        #     dici = {}
        #     id += 1
        #     x,y,w,h = face[0],face[1],face[2],face[3]
        #     dici['id'] = id
        #     dici['data'] = [x,y,w,h]
        #     rects.append(dici)

        # biggest = None
        # biggest_w = 0

        # for i in rects:
        #     if i['data'][2] > biggest_w:
        #         biggest = i
        #         biggest_w = i['data'][2]

        if listener.getGesture() == 'swipe_up' and swipecooldown == 0:
            resetReactions()
            print 'Swiping up'
            cmd = """
            osascript -e 'tell application "System Events" to keystroke "j"'
            """
            os.system(cmd)
            # tab.evaluate("$('html, body').animate({scrollTop: '+=500px'}, 1000);")
            listener.resetGesture()
            swipecooldown = 3
            gesturecooldown += 5

        elif listener.getGesture() == 'swipe_down' and swipecooldown == 0:
            resetReactions()
            print 'Swiping down'
            # tab.evaluate("$('html, body').animate({scrollTop: '-=500px'}, 1000);")
            cmd = """
            osascript -e 'tell application "System Events" to keystroke "k"'
            """
            os.system(cmd)
            listener.resetGesture()
            swipecooldown = 3
            gesturecooldown += 5

        elif listener.getGesture() == 'heart' and gesturecooldown == 0:
            resetReactions()
            print 'Clicking loved it'
            tab.evaluate('clickReaction("amei")')
            listener.resetGesture()
            gesturecooldown = 30

        elif listener.getGesture() == 'thumbsup' and gesturecooldown == 0:
            resetReactions()
            print 'Clicking thumbs up'
            tab.evaluate('clickReaction("curtir")')
            listener.resetGesture()
            gesturecooldown = 30

        # print 'Cooldown:', cooldown
        emotion_name = 0    
        # if biggest != None:
        #     x = biggest['data'][0]
        #     y = biggest['data'][1]
        #     w = biggest['data'][2]
        #     h = biggest['data'][3]

        #     cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        #     roi_gray = gray[y:y+h, x:x+w]
        #     roi_color = frame[y:y+h, x:x+w]

        #     cut = cv2.resize(roi_gray, (350, 350))
        #     # emotion_name = fisherFace.predict(cut)[0]
            
        cv2.putText(frame,str(exp),(200,100), font, 2,(255,0,0),3, cv2.LINE_AA)

        #     reactions[emotions[emotion_name]] += 1

        # e = process.stdout.readline()
        # print(e.strip().split())
        # if (e[0] in emotions):
        #     reactions[e[0]] += 1

        keys = reactions.keys()

        # print(reactions)
        
        if emotions[emotion_name] != 'neutral':
            reactions['neutral'] -= 2

        for key in keys:
            # print key,reactions[key]
            if reactions[key] >= 3 and key == "anger":
                resetReactions()
                if gesturecooldown == 0:
                    print 'Grr!'
                    tab.evaluate("clickReaction('grr');");
                    gesturecooldown = 20

            if reactions[key] >= 3 and key == "surprise":
                resetReactions()
                if gesturecooldown == 0:
                    print 'Uau!'
                    tab.evaluate("clickReaction('uau');");
                    gesturecooldown = 20

            if reactions[key] >= 3 and key == "happy":
                resetReactions()
                if gesturecooldown == 0:
                    print 'Haha!'
                    tab.evaluate("clickReaction('haha');");
                    gesturecooldown = 20

            if reactions[key] >= 3 and key == "sadness":
                resetReactions()
                if gesturecooldown == 0:
                    print 'Sad'
                    tab.evaluate("clickReaction('triste');");
                    gesturecooldown = 20

            if reactions[key] == 30 and key == "neutral":
                resetReactions()

        # Display the resulting frame
        cv2.imshow('Camera',frame)
        # print("No circles were found")

        swipecooldown -= 1
        gesturecooldown -= 1

        if swipecooldown <= 0:
            swipecooldown = 0
        if gesturecooldown <= 0:
            gesturecooldown = 0

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        if cv2.waitKey(25) & 0xFF == ord('r'):
            resetReactions()
        #except:
            # controller.remove_listener(listener)
            # screen.onScriptStopped()
            # print "Chrome is unresponsive or has been closed"
            # screen.updateText("Chrome is unresponsive \n or has been closed\n Please try again")
            # cap.release()
            # cv2.destroyAllWindows()
            # jqueryIsInjected = False
            # break
        time.sleep(0.005)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def resetReactions():
    print 'resetting'
    reactions["happy"] = 0
    reactions["surprise"] = 0
    reactions["sadness"] = 0
    reactions["anger"] = 0
    reactions["neutral"] = 0

begin()
# screen = Screen()
# screen.setFn(begin)k
# screen.start()
