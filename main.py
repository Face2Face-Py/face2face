#!/usr/bin/env python
__author__      = "Matheus Dib, Fabio de Miranda"

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
from select import select
from pprint import pprint

#JS CODE
# a = $(".UFILikeLink._4x9-._4x9_._48-k:visible")
# for (i=0;i<a.length;i++){
# 	console.log(a[i])
#     console.log($(a[i]).isVisible());
# }

osversion = None

if platform.system() == "Windows":
    osversion = "windows"
    print 'Killing all chrome instances'
    subprocess.Popen('TASKKILL /IM chrome.exe /F')
    time.sleep(1)
    chromedir = '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222'
    print 'opening chrome with permissions'
    subprocess.Popen(chromedir)
    print 'chrome open'

elif platform.system() == "Darwin":
    osversion = "mac"
    os.system("pkill Chrome")
    time.sleep(2)
    os.system("open /Applications/Google\ Chrome.app --args --remote-debugging-port=9222")
    time.sleep(2)
else:
    print "OS not supported"
# If you want to open a video, just change this path
#cap = cv2.VideoCapture('hall_box_battery.mp4')

print 'load remote debugging'
# Parameters to use when opening the webcam.
cap = cv2.VideoCapture(0)
cv2.setUseOptimized(True)
chrome = Chromote()
print chrome.host
print chrome.port
# for i in chrome.tabs:
#     if chrome.tabs.index(i) != 0:
#         print "please close all other tabs"
tab = chrome.tabs[0]
tab.set_url("https://www.facebook.com/")

isvisiblefn = """
$.fn.isVisible = function() {
    var rect = this[0].getBoundingClientRect();
    return (
        (rect.height > 0 || rect.width > 0) &&
        rect.bottom >= 0 &&
        rect.right >= 0 &&
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.left <= (window.innerWidth || document.documentElement.clientWidth)
    );
};
"""

returnObjfn = """
function returnObj(a) {
     b = {};
     for (i=0;i<a.length;i++){
         c = [];
         c[0] = a[i]
         c[1] = $(a[i]).isVisible()
         b[i] = c;
 }
    return b;
};
"""



# createobjstr = """
#
# ""

# tab.evaluate('for (i=0;i<a.length;i++){console.log(a[i]);console.log($(a[i]).isVisible());}')
forstr = """
for (i=0;i<a.length;i++){
    ($(a[i]).isVisible());
}
"""

print "Please enable JQuery injection and then press OK!"
tab.evaluate('window.confirm("Please inject jQuery and then press OK");')
time.sleep(2)

try:
    with open('script.js', 'r') as content_file:
        content = content_file.read()
        tab.evaluate(content)

    tab.evaluate("console.log('Jquery is' + typeof jQuery)")
    isloaded = tab.evaluate("typeof jQuery")
except:
    print "an error ocurred"
    raise SystemExit

json_string = isloaded
obj = json.loads(json_string)

if obj["result"]["result"]["value"] != "function":
    print "JQuery was not injected... Exiting"
    if osversion == "mac":
        os.system("pkill Chrome")
    elif osversion == "windows":
        subprocess.Popen('TASKKILL /IM chrome.exe /F')
    raise SystemExit

else:
    print "Functions properly injected"

mon = {'top': 160, 'left': 160, 'width': 400, 'height': 400}
sct = mss()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
font = cv2.FONT_HERSHEY_SIMPLEX
lower = 0
upper = 1

def orientation(dx,dy):
    if dx>dy:
        return ("Horizontal")
    else:
        return ("Vertical")

# Returns an image containing the borders of the image
# sigma is how far from the median we are setting the thresholds
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

while(True):

    print "Amount of like buttons avaiable"
    print json.loads(tab.evaluate("countVisible()"))["result"]["result"]["value"]
    # tab.evaluate("clickReaction(0,'haha')")

    # Capture frame-by-frame
    # print("New frame")
    ret, frame = cap.read()

    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    imgRGB = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    cv2.imshow('test', np.array(imgRGB))

    # Display the resulting frame
    cv2.imshow('Detector de circulos',frame)
    # print("No circles were found")
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
