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
    tab.evaluate(isvisiblefn)
    tab.evaluate(returnObjfn)
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
    # forret = tab.evaluate("returnObj($('.UFILikeLink._4x9-._4x9_._48-k:visible'))")
    likeall = tab.evaluate('''
    z = returnObj($('.UFILikeLink._4x9-._4x9_._48-k:visible'))
    for (i=0;i<Object.keys(z).length;i++){
    	// console.log(z[i][0]);
        // console.log()
    	// console.log(z[i][1]);
    	if (z[i][1] == true && $(z[i][0]).attr("data-testid") == "fb-ufi-likelink"){
            z[i][0].click();
            console.log("Clicking on next sibling")
            console.log(z[i][0].nextSibling)
            z[i][0].nextSibling.click()
        }
    }
    ''')
    # Capture frame-by-frame
    # print("New frame")
    ret, frame = cap.read()

    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    imgRGB = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    cv2.imshow('test', np.array(imgRGB))

    # a = "a = $('.UFILikeLink._4x9-._4x9_._48-k:visible');"
    # tab.evaluate(a)
    # # Convert the frame to grayscale
    # # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # A gaussian blur to get rid of the noise in the image
    # # blur = cv2.GaussianBlur(gray,(5,5),0)
    # # # Detect the edges present in the image
    # # bordas = auto_canny(blur)
    #
    # hpixel = 235
    # d = 38
    # h = 6.3
    # f = (hpixel*d)/h
    #
    # circles = []
    #
    #
    # # Obtains a version of the edges image where we can draw in color
    # bordas_color = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)
    #
    # coordlistx=[]
    # coordlisty=[]
    # radiuslist=[]
    #
    # # HoughCircles - detects circles using the Hough Method. For an explanation of
    # # param1 and param2 please see an explanation here http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
    # circles=cv2.HoughCircles(bordas,cv.HOUGH_GRADIENT,2,40,param1=50,param2=100,minRadius=5,maxRadius=60)
    # if circles != None and len(circles) <= 3:
    #     circles = np.uint16(np.around(circles))
    #
    #     for i in circles[0,:]:
    #         stdradius = i[2]
    #         radiuslist.append(stdradius)
    #
    #     mean = np.mean(stdradius)
    #
    #     checker = False
    #     #
    #     # for j in circles[0,:]:
    #
    #     for i in circles[0,:]:
    #         if (len(circles[0,:])) != 3:
    #             checker = False
    #             break
    #         if i[2] in range(int(mean-10),int(mean+10)):
    #             checker = True
    #         else:
    #             break
    #
    #         stdradius = i[2]
    #         # coordlistx.append([i[0],i[1]])
    #         coordlistx.append(int(i[0]))
    #         coordlisty.append(int(i[1]))
    #         d2 = f*h/(i[2]*4)
    #         # draw the outer circle
    #         # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
    #         if checker == True:
    #             cv2.circle(bordas_color,(i[0],i[1]),i[2],(0,255,0),2)
    #             cv2.circle(bordas_color,(i[0],i[1]),2,(0,0,255),3)
    #
    #
    #         # draw the center of the circle
    #
    #
    #
    # if len(coordlistx) > 2:
    #     dx = max(coordlistx) - min(coordlistx)
    #     dy = max(coordlisty) - min(coordlisty)
    #     #
    #     #     print("Ta na horizontal")
    #     # else:
    #     #     print("Ta na vertical")
    #     b = ("Distancia: {0} cm Orientacao: {1}").format(int(d2),orientation(dx,dy))
    #     # cv2.putText(bordas_color,b,(0,50), font, 1,(0,0,255),1,cv2.AA)
    #
    #
    # # Draw a diagonal blue line with thickness of 5 px
    # # cv2.line(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
    # # cv2.line(bordas_color,(0,0),(511,511),(255,0,0),5)
    #
    # # cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
    # # cv2.rectangle(bordas_color,(384,0),(510,128),(0,255,0),3)
    #
    # # cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    #
    # # cv2.putText(bordas_color,b,(0,50), font, 0.5,(255,255,255),2,cv2.CV_AA)
    #
    # #More drawing functions @ http://docs.opencv.org/2.4/modules/core/doc/drawing_functions.html


    # Display the resulting frame
    cv2.imshow('Detector de circulos',frame)
    # print("No circles were found")
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    # Dizer a distancia

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
