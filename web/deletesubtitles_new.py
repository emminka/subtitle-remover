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
import keras_ocr
from difflib import SequenceMatcher

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
fpska = video.get(cv2.CAP_PROP_FPS) #pocet fps za sekundu

pipeline = keras_ocr.pipeline.Pipeline()
f = open('output.txt','w') #zapisujem ake su titulky
poleObrazkov = []
fps_total = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #pocet framov celeho video
video = cv2.VideoCapture(filepath)
videocap = cv2.VideoCapture(filepath)
#fpska = video.get(cv2.CAP_PROP_FPS)
counting_frames = 1
count = 0
cislo_frame = 1
images = []

text_aktual = []
text_predch = []

start_tit = 0
koniec_tit = 0

titulky_konkretne = []

koncovka = "_noSUB_noSOUND.mp4"
new_name_same_path = filepath.rsplit(".", 1)[0];
new_name_same_path += koncovka;
print(new_name_same_path)

koncovka1 = "_noSUB_yesSOUND.mp4"
new_name_same_path1 = filepath.rsplit(".", 1)[0];
new_name_same_path1 += koncovka1;

mask = np.zeros((heightOfVideo,widthOfVideo,3),np.uint8) #vykreslenie ciernej masky v rozmeroch videa

output = cv2.VideoWriter(new_name_same_path, -1, fpska, (widthOfVideo,heightOfVideo)) #vysledne video

cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape

gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) #na premalovanie lebo inak sa to nevysvetlitelne stazuje
	

od_do_bool_stare = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
od_do_bool_nove = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
od_do_bool_stred = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
vsetky_titulky = []
kontrola_stare = 0
kontrola_nove = 0

def text_on_particular_frame(frame_number):
    videocap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    prediction_groups_bis = []
    success, image = videocap.read()
    if not success:
        return
    image = image[yL:yR,xL:xR]
    image = keras_ocr.tools.read(image)
    prediction_groups_bis = pipeline.recognize([image])
    particular_text = [text for text, _ in prediction_groups_bis[0]]
    #print(particular_text, "frame", frame_number)
    return(particular_text)

def find_exact_frame(start_frame,end_frame,start_text,end_text): #bisection

    global od_do_bool_nove
    global od_do_bool_stare
    global od_do_bool_stred
    global kontrola_nove
    global kontrola_stare

    print("ZACIATOCNY FRAME", start_frame)
    print("KONCOVY FRAME", end_frame)
    low_frame = start_frame
    high_frame = end_frame
    middle_frame = 0
    while low_frame < high_frame:
        # Calculate the middle frame
        #print("HLADAME ZACIATOK DRUHEHO TITULKU")
        middle_frame = (low_frame + high_frame) // 2
    
        text = text_on_particular_frame(middle_frame)

        s = SequenceMatcher(None, text, end_text)
        similarity = s.ratio()
        if text is None:
            podobnost_vlastna = 0.6
        elif len(text) <= 4:
            podobnost_vlastna = 0.2
        else:
            podobnost_vlastna = 0.6
        if similarity < podobnost_vlastna:
        # Text still doesn't match, update the search range
            low_frame = middle_frame + 1
            #print("text sa nezhoduje, zvyšujem frame")
        
        else:
        # Text matches, update the search range
            high_frame = middle_frame
            #print("text sa zhoduje, menim range")
            if (text == []):
                od_do_bool_nove[2]=0 #neodmazavam
            else:
                od_do_bool_nove[2]=1 #odmazavam

    # Print the frame where the end text starts
    print('KONCOVE TITULKY ZACINAJU NA', high_frame)
    od_do_bool_nove[0]=high_frame
    kontrola_nove=high_frame
    
    # Define the search range using the found frame and the end frame
    second_subtitle_start = high_frame
    low_frame = start_frame
    high_frame = second_subtitle_start

    while low_frame < high_frame:
        #print("HLADAME KONIEC PRVEHO TITULKU")
        # Calculate the middle frame
        middle_frame = (low_frame + high_frame) // 2

        text = text_on_particular_frame(middle_frame)

        # Calculate the similarity between the extracted text and the start text
        s = SequenceMatcher(None, text, start_text)
        similarity = s.ratio()

        if text is None:
            podobnost_vlastna = 0.6
        elif len(text) <= 4:
            podobnost_vlastna = 0.2
        else:
            podobnost_vlastna = 0.6

        if similarity < podobnost_vlastna:
            # Text still doesn't match, update the search range
            high_frame = middle_frame
            #print("text sa nezhoduje, znižujem frame")
        else:
            # Text matches, update the search range
            low_frame = middle_frame + 1
            #print("text sa zhoduje, menim trange")
            if (text == []):
                od_do_bool_stare[2]=0 #neodmazavam
            else:
                od_do_bool_stare[2]=1 #odmazavam


    # Print the frame where the start text ends
    print('PRVE TITULKY KONCIA NA', low_frame - 1)
    od_do_bool_stare[1]=(low_frame - 1)
    kontrola_stare=(low_frame - 1)

    
    vsetky_titulky.append(od_do_bool_stare[:])
    print("vsetky",vsetky_titulky,"stare",od_do_bool_stare, "nove", od_do_bool_nove)

    od_do_bool_stare = od_do_bool_nove

    od_do_bool_nove=[0,0,0]

    if(kontrola_stare+1 != kontrola_nove):
        od_do_bool_stred[0]=kontrola_stare+1
        od_do_bool_stred[1]=kontrola_nove-1
        vsetky_titulky.append(od_do_bool_stred[:])
        od_do_bool_stred=[0,0,0]

    print("vsetky",vsetky_titulky,"stare",od_do_bool_stare, "nove", od_do_bool_nove)


if methodOfRemoving == 1: #pouzivame keras
    success,image = videocap.read()
    while success:
        if(count<8):
            image = image[yL:yR,xL:xR]  #orazena image, od:do a od:do
            cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file 
            poleObrazkov.append(r'C:\Users\Emma\Desktop\Bakalarka\web\frame%d.jpg' % count)
            #print(poleObrazkov)
            cislo_frame += 30 #cca 30framov ma sekunda
            videocap.set(cv2.CAP_PROP_POS_FRAMES, cislo_frame)
            success,image = videocap.read()
        else:
            images = [keras_ocr.tools.read(img) for img in poleObrazkov]
            prediction_groups = pipeline.recognize(images)
            for x in range(len(images)):
                with open('output.txt', 'a') as f:
                    print("",file=f)
                    print("FRAME",counting_frames,"Z", fps_total, file=f)
                counting_frames = counting_frames + 30
                for text, box in prediction_groups[x]:
                    text_aktual.append(text)
                    with open('output.txt', 'a') as f:
                        print(text, file=f)

                s = SequenceMatcher(None, text_aktual, text_predch)
                similarity = s.ratio()

                if((counting_frames-30) != 1):
                    print((counting_frames -60)," je",text_predch,"a", (counting_frames - 30), "je", text_aktual)
                    if similarity >= 0.6:
                        print("Text sa zhoduje alebo je veľmi podobný.")
                        od_do_bool_stare[1]=(counting_frames - 30)
                    else:
                        print("Text sa nezhoduje.")
                        prvy_frame = counting_frames - 60
                        druhy_frame = counting_frames - 30

                        od_do_bool_stare[1]=(counting_frames - 60)
                        od_do_bool_nove[1]=(counting_frames - 30)

                        find_exact_frame(prvy_frame,druhy_frame,text_predch,text_aktual)#VOLAME FUNKCIU NA BISEKCIU

                    text_predch = text_aktual
                    text_aktual = []
                else:
                    od_do_bool_stare[0]=1
                    text_predch = text_aktual
                    text_aktual = []
            count = -1
            poleObrazkov = []
            images = []
            prediction_groups = []
        #print('Read a new frame: ', success)
        count += 1
    if not poleObrazkov:
        print("Pole obr prazdne,nerobime nic")
    else:
        images = [keras_ocr.tools.read(img) for img in poleObrazkov]
        prediction_groups = pipeline.recognize(images)
        for x in range(len(images)):
            with open('output.txt', 'a') as f:
                print("",file=f)
                print("FRAME",counting_frames,"Z", fps_total, file=f)
            counting_frames = counting_frames + 30
            for text, box in prediction_groups[x]:
                text_aktual.append(text)
                with open('output.txt', 'a') as f:
                    print(text, file=f)

            s = SequenceMatcher(None, text_aktual, text_predch)
            similarity = s.ratio()

            if((counting_frames-30) != 1):
                print((counting_frames -60)," je",text_predch,"a", (counting_frames - 30), "je", text_aktual)
                if similarity >= 0.6:
                    print("Text sa zhoduje alebo je veľmi podobný.")
                    od_do_bool_stare[1]=(counting_frames - 30)
                else:
                    print("Text sa nezhoduje.")
                    prvy_frame = counting_frames - 60
                    druhy_frame = counting_frames - 30

                    od_do_bool_stare[1]=(counting_frames - 60)
                    od_do_bool_nove[1]=(counting_frames - 30)

                    find_exact_frame(prvy_frame,druhy_frame,text_predch,text_aktual)

                text_predch = text_aktual
                text_aktual = []
            else:
                od_do_bool_stare[0]=1
                text_predch = text_aktual
                text_aktual = []

    od_do_bool_stare[1]=fps_total-1 #pocetframov
    vsetky_titulky.append(od_do_bool_stare[:])
    print("vsetky",vsetky_titulky)


if (video.isOpened()== False): 
    print("Error opening video file")

while(video.isOpened()):
    if methodOfRemoving == 0:
        ret, frame = video.read()
        # Capture frame-by-frame
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
    else:
        ret, frame = video.read()
        if ret == True:
            # Get the current frame number
            frame_number = int(video.get(cv2.CAP_PROP_POS_FRAMES))

            # Loop through the title ranges to see if the current frame is within a title range
            found_title_range = False
            for title_start, title_end, title_bool in vsetky_titulky:
                if frame_number >= title_start and frame_number <= title_end and title_bool == 1:
                    found_title_range = True
                    break
            
            # If the current frame is not within a title range, write it to the output with no modifications
            if not found_title_range:
                output.write(frame)
            # If the current frame is within a title range, modify it as needed
            else:
                no_subtitles_frame = cv2.inpaint(frame,gray_mask,3,cv2.INPAINT_TELEA)
                output.write(no_subtitles_frame)

                # Check if the next frame is in the subtitle range immediately following a title range with bool 1
                if len(vsetky_titulky) > 1:
                    next_title_start, next_title_end, next_title_bool = vsetky_titulky[1]
                    if frame_number == title_end and next_title_bool == 0:
                        video.read() # skip the next frame
        else:
            break
        

cv2.destroyAllWindows()

output.release()

audio_clip = AudioFileClip(filepath)   #audio ziskavam lebo cv2 nepouziva
modified_clip = VideoFileClip(new_name_same_path)
final_clip = modified_clip.set_audio(audio_clip)
final_clip.write_videofile(new_name_same_path1)
os.remove(new_name_same_path)


print("Video has been released.")


