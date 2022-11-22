import cv2
import numpy as np


uploadedVideo = cv2.VideoCapture(r"C:\Users\Emma\Desktop\Bakalarka\titulky_vyssie.mp4")
output = cv2.VideoWriter('output.mp4', -1, 30.0, (1920,1080))


success,frame = uploadedVideo.read()
count = 0

if (uploadedVideo.isOpened()== False): 
    print("Error opening video file")

while(uploadedVideo.isOpened()):
    # Capture frame-by-frame
    success, frame = uploadedVideo.read()
    if success == True:
        #cv2.imshow('Frame', image)
        #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
        #success,image = vidcap.read()
        #print('Read a new frame: ', success)
        count += 1
        output.write(frame)


    else: 
        break
        
print("omg yes ide to")


uploadedVideo.release()
cv2.destroyAllWindows()
output.release()


