import sys,json
import cv2
import numpy as np
import random
from random import randrange
import time


print("Command executed from Python script")
sys.stdout.flush()

data = sys.stdin.readlines()
data = json.loads(data[0])
print(data[0]+10)
sys.stdout.flush()

#pomocou inpaint
#naosbime krat 2,13
#titulky_vyssie

video = cv2.VideoCapture(r"C:\Users\Emma\Desktop\Bakalarka\videos\titulky_vyssie.mp4")
mask = cv2.imread(r"C:\Users\Emma\Desktop\Bakalarka\web\black.png")
xL = 121
yL= 831
xR = 1781
yR = 910


output = cv2.VideoWriter('output.mp4', -1, 30.0, (1920,1080))

cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape

gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	
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
        

        dst = cv2.inpaint(frame,gray_mask,3,cv2.INPAINT_TELEA)
        
        #cv2.imshow('Frame', dst)
        #vyplnit_mi(1,"random")

        #cv2.rectangle(frame, (xL, yL), (xR, yR),(73, 116, 164), -1)

        output.write(dst)

        # Display the resulting frame
        cv2.imshow('Frame', dst)
        
        
    else: 
        break

video.release()
#cv2.destroyAllWindows()
output.release()

