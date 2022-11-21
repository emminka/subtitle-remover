import cv2
import numpy as np
import random
from random import randrange
import time
import sys
import getopt

#Lx = a
#LY = b
#Rx = c
#Ry = d


xL = None
yL = None
xR = None
yR = None
filepath = None

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "a:b:c:d:e:")
    
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
         
    
if(xL is None or yL is None or xR is None or yR is None or filepath is None):
    print("dovidopo exitujeeme ,daco  je plano")
    sys.exit(1)

#print( xL +" " + yL+" " +xR+" " +yR)
print(type(xL))
print(type(xR))
  


#pomocou inpaint
#naosbime krat 2,13
#titulky_vyssie

video = cv2.VideoCapture(filepath)
mask = cv2.imread(r"C:\Users\Emma\Desktop\Bakalarka\web\black.png")




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

