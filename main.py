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
from select import select
from pprint import pprint


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

    print "waiting 5 secs"
    time.sleep(8)

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
        jqueryIsInjected = True
        tab.evaluate("onPageLoaded();")

    mon = {'top': 160, 'left': 160, 'width':200, 'height': 200}
    sct = mss()

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    font = cv2.FONT_HERSHEY_SIMPLEX
    lower = 0
    upper = 1

    while(jqueryIsInjected == True):
        try:
            print chrome
            tab.evaluate("showSelected()")
            # tab.evaluate("clickReaction('grr')")
            # counterval = json.loads(counter)["result"]["result"]["value"]
            # print "Amount of like buttons avaiable " + str(counterval)
            # Capture frame-by-frame
            # print("New frame")

            ret, frame = cap.read()

            sct.get_pixels(mon)
            img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
            imgRGB = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            # cv2.imshow('test', np.array(imgRGB))

            # tab.evaluate("clickReaction(0,'haha')")
            # Display the resulting frame
            cv2.imshow('Camera',frame)
            # print("No circles were found")
            time.sleep(0.25)

            if cv2.waitKey(50) & 0xFF == ord('q'):
                break

        except:
            screen.onScriptStopped()
            print "Chrome is unresponsive or has been closed"
            screen.updateText("Chrome is unresponsive \n or has been closed\n Please try again")
            cap.release()
            cv2.destroyAllWindows()
            jqueryIsInjected = False

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

mainthread = threading.Thread(target=begin)

screen = Screen()
screen.setFn(begin)
screen.start()

# mainthread.start()
# mainThread = Thread(target=screen.start)
# mainThread.start()
