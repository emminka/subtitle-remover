import cv2
import os
import numpy as np
import random
from random import randrange
import time
import sys
import getopt
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

xL = None #suradnice z aplikacie
yL = None
xR = None
yR = None
filepath = None
heightOfVideo = None
widthOfVideo = None

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "a:b:c:d:e:f:g:h:")
    
except:
    print("Error")

for opt, arg in opts:
    if opt in ['-a']:
        xL = int(arg)
        print("zapisujem lave x", xL)
    elif opt in ['-b']:
        yL = int(arg)
        print("zapisujem lave y",yL)
    elif opt in ['-c']:
        xR = int(arg)
        print("zapisujem prave x",xR)
    elif opt in ['-d']:
        yR = int(arg)  
        print("zapisujem prave y", yR)
    elif opt in ['-e']:
        filepath = arg  
        print("cesticka", filepath)
    elif opt in ['-f']:
        heightOfVideo = int(arg)
        print("heightOfVideo", heightOfVideo)
    elif opt in ['-g']:
        widthOfVideo = int(arg)  
        print("widthOfVideo", widthOfVideo)
    elif opt in ['-h']:
        methodOfRemoving = int(arg)  
        print("sposob odstranenia", methodOfRemoving); #0 default, 1 keras
         
if(xL is None or yL is None or xR is None or yR is None or filepath is None or heightOfVideo is None or  widthOfVideo is None or methodOfRemoving is None):
    print("dovidopo exitujeeme ,daco  je plano")
    sys.exit(1)


video = cv2.VideoCapture(filepath)
fpska = video.get(cv2.CAP_PROP_FPS)

koncovka = "_noSUB_noSOUND.mp4"
new_name_same_path = filepath.rsplit(".", 1)[0];
new_name_same_path += koncovka;
print(new_name_same_path)

koncovka1 = "_noSUB_yesSOUND.mp4"
new_name_same_path1 = filepath.rsplit(".", 1)[0];
new_name_same_path1 += koncovka1;

mask = np.zeros((heightOfVideo,widthOfVideo,3),np.uint8) #vykreslenie ciernje masky v rozmeroch videa

output = cv2.VideoWriter(new_name_same_path, -1, fpska, (widthOfVideo,heightOfVideo)) #vysledne video

cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape

gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) #na premalovanie lebo inak sa to nevysvetlitelne stazuje
	

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

audio_clip = AudioFileClip(filepath)   #audio ziskavam lebo cv2 nepouziva
modified_clip = VideoFileClip(new_name_same_path)
final_clip = modified_clip.set_audio(audio_clip)
final_clip.write_videofile(new_name_same_path1)
os.remove(new_name_same_path)


print("Video has been released.")

