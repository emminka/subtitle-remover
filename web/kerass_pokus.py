import matplotlib.pyplot as plt
import cv2
import keras_ocr
import os
import time
import sys
from difflib import SequenceMatcher

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.


pipeline = keras_ocr.pipeline.Pipeline()
filepath =  r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\titulky.mp4'

f = open('output.txt','w')

poleObrazkov = []
text_aktual = []
text_predch = []

video = cv2.VideoCapture(filepath)

fpska = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #pocet framov celeho video
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
dolna_tretina_vyska =int(2*(height/3))
prva_desatina_sirky=int(width/10)
posledna_desatina_sirky=int(9*(width/10))
counting_frames = 1
success,image = video.read()
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
        video.set(cv2.CAP_PROP_POS_FRAMES, cislo_frame)
        success,image = video.read()
    else:
        images = [keras_ocr.tools.read(img) for img in poleObrazkov]
        prediction_groups = pipeline.recognize(images)
        for x in range(len(images)):
            with open('output.txt', 'a') as f:
                print("",file=f)
                print("FRAME",counting_frames,"Z", fpska, file=f)
            counting_frames = counting_frames + 30
            for text, box in prediction_groups[x]:
                text_aktual.append(text)
                with open('output.txt', 'a') as f:
                    print(text, file=f)

            s = SequenceMatcher(None, text_aktual, text_predch)
            similarity = s.ratio()

            if((counting_frames-30) != 1):
                print("porovnavam", (counting_frames -60) , "a ", (counting_frames - 30))
                print("predch je",text_predch,"akutal je", text_aktual)
                if similarity >= 0.7:
                    print("Text sa zhoduje alebo je veľmi podobný.")
                else:
                    print("Text sa nezhoduje.")

                text_predch = text_aktual
                text_aktual = []

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
            print("FRAME",counting_frames,"Z", fpska, file=f)
        counting_frames = counting_frames + 30
        for text, box in prediction_groups[x]:
            text_aktual.append(text)
            with open('output.txt', 'a') as f:
                print(text, file=f)

        s = SequenceMatcher(None, text_aktual, text_predch)
        similarity = s.ratio()

        if((counting_frames-30) != 1):
            print("porovnavam", (counting_frames -60) , "a ", (counting_frames - 30))
            print("predch je",text_predch,"akutal je", text_aktual)
            if similarity >= 0.7:
                print("Text sa zhoduje alebo je veľmi podobný.")
            else:
                print("Text sa nezhoduje.")

            text_predch = text_aktual
            text_aktual = []
    


