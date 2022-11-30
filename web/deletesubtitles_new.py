import cv2
import numpy as np
import random
from random import randrange
import time
import sys
import getopt
import matplotlib.pyplot as plt

xL = None #suradnice z aplikacie
yL = None
xR = None
yR = None
filepath = None
heightOfVideo = None
widthOfVideo = None

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "a:b:c:d:e:f:g:")
    
except:
    print("Error")

for opt, arg in opts:
    if opt in ['-a']:
        xL = int(arg)
        print("zapisujem lave x", xL);
    elif opt in ['-b']:
        yL = int(arg)
        print("zapisujem lave y",yL);
    elif opt in ['-c']:
        xR = int(arg)
        print("zapisujem prave x",xR);
    elif opt in ['-d']:
        yR = int(arg)  
        print("zapisujem prave y", yR);
    elif opt in ['-e']:
        filepath = arg  
        print("cesticka", filepath);
    elif opt in ['-f']:
        heightOfVideo = int(arg)
        print("heightOfVideo", heightOfVideo);
    elif opt in ['-g']:
        widthOfVideo = int(arg)  
        print("widthOfVideo", widthOfVideo);
         
if(xL is None or yL is None or xR is None or yR is None or filepath is None):
    print("dovidopo exitujeeme ,daco  je plano")
    sys.exit(1)


video = cv2.VideoCapture(filepath)

koncovka = "_no_subtitles.mp4"
new_name_same_path = filepath.rsplit(".", 1)[0];
new_name_same_path += koncovka;

mask = np.zeros((heightOfVideo,widthOfVideo,3),np.uint8) #vykreslenie ciernje masky v rozmeroch videa

output = cv2.VideoWriter(new_name_same_path, -1, 30.0, (widthOfVideo,heightOfVideo)) #vysledne video

cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape

gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) #na premalovanie lebo inak sa to nevysvetlitelne stazuje
	
#cv2.imshow('image', mask)

if (video.isOpened()== False): 
    print("Error opening video file")

while(video.isOpened()):
    # Capture frame-by-frame
    ret, frame = video.read()
    if ret == True:
        # Press Q on keyboard to  exit
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        no_subtitles_frame = cv2.inpaint(frame,gray_mask,3,cv2.INPAINT_TELEA) #pomocou inpaint odstranujem (iba zamazavam) titulky
        output.write(no_subtitles_frame)
        # Display the resulting frame
        # cv2.imshow('Frame', dst)   
    else: 
        break
#video.release()
cv2.destroyAllWindows()
output.release()
print("Video has been released.")

