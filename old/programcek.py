import cv2
import numpy as np
import random
from random import randrange


video = cv2.VideoCapture("test.mp4")

output = cv2.VideoWriter('output.mp4', -1, 30.0, (1920,1080))



if (video.isOpened()== False): 
    print("Error opening video file")


def vyplnit_mi(poloha,farba_co_chcem):
    # adding filled rectangle on each frame
    farby_vsetky = {
        "modra": (204, 142, 0),
        "zelena": (59, 139, 75),
        "cervena": (0, 0, 157),
        "zlta": (42, 235, 255),
        "ruzova": (180, 105, 180),
        "fialova": (200, 162, 200),
        "hneda": (73, 116, 164),
        "cierna": (0, 0, 0),
        "biela": (255, 255, 255),
        }


    x1 = randrange(1920)
    y1 = randrange(1080)
    x2 = randrange(1920)
    y2 = randrange(1080)

    if farba_co_chcem == "random":
        farba_pls, capital = random.choice(list(farby_vsetky.items()))
        cv2.rectangle(frame, (x1, y1), (x2, y2),(farby_vsetky[farba_pls]), -1)

    else:
        cv2.rectangle(frame, (100, 150), (500, 600), (farby_vsetky[farba_co_chcem]), -1)
        
    

while(video.isOpened()):
    # Capture frame-by-frame
    ret, frame = video.read()
    
    
    if ret == True:

        # Press Q on keyboard to  exit
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        
        vyplnit_mi(1,"random")

        output.write(frame)

        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        

    else: 
        break

video.release()
cv2.destroyAllWindows()
output.release()

