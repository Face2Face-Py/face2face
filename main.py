#!/usr/bin/env python
__author__      = "Raphael Costa,Bruna Kimura,Frederico Curti,Elisa Malzoni"

import cv2
import cv2 as cv
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
import leapmotion as lm
import Leap


def begin():
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
    cap = cv2.VideoCapture(0)
    cv2.setUseOptimized(True)
    chrome = Chromote()

    # for i in chrome.tabs:
    #     if chrome.tabs.index(i) != 0:
    #         print "please close all other tabs"
    tab = chrome.tabs[0]
    tab.set_url("https://www.facebook.com/")

    print "waiting 15 secs"
    time.sleep(20)

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

    time.sleep(5)


    try:
        print "trying to inject script"
        with open('script.js', 'r') as content_file:
            content = content_file.read()
            tab.evaluate(content)

        tab.evaluate("console.log('Jquery is ' + typeof jQuery)")
        isloaded = tab.evaluate("typeof jQuery")
    except:
        print "an error ocurred"
        raise SystemExit

    time.sleep(1)
    

    json_string = isloaded
    obj = json.loads(json_string)

    print "checking if injection was successful"

    if obj["result"]["result"]["value"] != "function":
        print "JQuery was not injected... Exiting"

        jqueryIsInjected = False
        if osversion == "mac":
            os.system("pkill Chrome")
        elif osversion == "windows":
            subprocess.Popen('TASKKILL /IM chrome.exe /F')

        screen.updateText('There was an error\n when loading JQuery.\n Please try again')
        screen.onScriptStopped()
        # raise SystemExit

    else:
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
        
        jqueryIsInjected = True
        tab.evaluate("onPageLoaded();")

    mon = {'top': 160, 'left': 160, 'width':200, 'height': 200}
    sct = mss()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    font = cv2.FONT_HERSHEY_SIMPLEX
    lower = 0
    upper = 1

    swipecooldown = 10
    gesturecooldown = 50

    while(jqueryIsInjected == True):
        try:
        # tab.evaluate("showSelected()")
        # tab.evaluate("clickReaction('grr')")
        # counterval = json.loads(counter)["result"]["result"]["value"]
        # print "Amount of like buttons avaiable " + str(counterval)
        # Capture frame-by-frame
        # print("New frame")

            ret, frame = cap.read()
            
            if listener.getGesture() == 'swipe_up' and swipecooldown == 0:
                print 'Swiping up'
                cmd = """
                osascript -e 'tell application "System Events" to keystroke "j"' 
                """
                os.system(cmd)
                # tab.evaluate("$('html, body').animate({scrollTop: '+=500px'}, 1000);")
                listener.resetGesture()
                swipecooldown = 5
                gesturecooldown += 5
            elif listener.getGesture() == 'swipe_down' and swipecooldown == 0:
                print 'Swiping down'
                # tab.evaluate("$('html, body').animate({scrollTop: '-=500px'}, 1000);")
                cmd = """
                osascript -e 'tell application "System Events" to keystroke "k"' 
                """
                os.system(cmd)
                listener.resetGesture()
                swipecooldown = 5
                gesturecooldown += 5
            elif listener.getGesture() == 'heart' and gesturecooldown == 0:
                print 'Clicking loved it'
                tab.evaluate('clickReaction("amei")')
                listener.resetGesture()
                gesturecooldown = 40
            elif listener.getGesture() == 'thumbsup' and gesturecooldown == 0:
                print 'Clicking thumbs up'
                tab.evaluate('clickReaction("curtir")')
                listener.resetGesture()
                gesturecooldown = 40

            swipecooldown -= 1
            gesturecooldown -= 1
            
            if swipecooldown <= 0:
                swipecooldown = 0
            if gesturecooldown <= 0:
                gesturecooldown = 0

            # print 'Cooldown:', cooldown

            # Display the resulting frame
            cv2.imshow('Camera',frame)
            # print("No circles were found")

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        except:
            controller.remove_listener(listener)
            screen.onScriptStopped()
            print "Chrome is unresponsive or has been closed"
            screen.updateText("Chrome is unresponsive \n or has been closed\n Please try again")
            cap.release()
            cv2.destroyAllWindows()
            jqueryIsInjected = False
            break

    # When everything done, release the capture
    controller.remove_listener(listener)
    cap.release()
    cv2.destroyAllWindows()

screen = Screen()
screen.setFn(begin)
screen.start()
