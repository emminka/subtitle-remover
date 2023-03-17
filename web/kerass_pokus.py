import matplotlib.pyplot as plt
import cv2
import keras_ocr
import os
import time
import sys
# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.


pipeline = keras_ocr.pipeline.Pipeline()
filepath =  r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\titulky.mp4'

f = open('output.txt','w')

poleObrazkov = []
poleObrazkov2 = []
vidcap = cv2.VideoCapture(filepath)

length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) #pocet framov celeho video
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
dolna_tretina_vyska =int(2*(height/3))
prva_desatina_sirky=int(width/10)
posledna_desatina_sirky=int(9*(width/10))
counting_frames = 1
success,image = vidcap.read()
count = 0
cislo_frame = 1
images = []
while success:
    if(count<8):
        image = image[dolna_tretina_vyska:height,prva_desatina_sirky:posledna_desatina_sirky]  #orazena image, od:do a od:do
        cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file 
        poleObrazkov.append(r'C:\Users\Emma\Desktop\Bakalarka\web\frame%d.jpg' % count)
        print(poleObrazkov)
        cislo_frame += 30 # i.e. at 30 fps, this advances one second
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, cislo_frame)
        success,image = vidcap.read()
    else:
        images = [keras_ocr.tools.read(img) for img in poleObrazkov]
        prediction_groups = pipeline.recognize(images)
        for x in range(len(images)):
            with open('output.txt', 'a') as f:
                print("",file=f)
                print("FRAME",counting_frames,"Z", length, file=f)
            counting_frames = counting_frames + 30
            for text, box in prediction_groups[x]:
                with open('output.txt', 'a') as f:
                    print(text, file=f)

        count = -1
        poleObrazkov = []
        images = []
        prediction_groups = []

    print('Read a new frame: ', success)
    count += 1

if not poleObrazkov:
    print("Pole obr prazdne,nerobime nic")
else:
    images = [keras_ocr.tools.read(img) for img in poleObrazkov]
    prediction_groups = pipeline.recognize(images)
    for x in range(len(images)):
        with open('output.txt', 'a') as f:
            print("",file=f)
            print("FRAME",counting_frames,"Z", length, file=f)
        counting_frames = counting_frames + 30
        for text, box in prediction_groups[x]:
            with open('output.txt', 'a') as f:
                print(text, file=f)


