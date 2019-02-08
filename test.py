import subprocess
import time
import sys

# p = subprocess.Popen(['/usr/local/bin/python3', 'Real-Time-Facial-Expression-Recognition-with-DeepLearning/webcam/webcam_detection.py'], universal_newlines=True, stdout=subprocess.PIPE, bufsize=1)
p = subprocess.Popen(['/usr/local/bin/python3', 'oi.py'], stdout=subprocess.PIPE, bufsize=1)

while True:
    print(p.stdout.readline())
    time.sleep(1)