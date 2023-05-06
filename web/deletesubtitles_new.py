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
import time
import argparse
import datetime

start_time = time.time() #for info how long it takes
xL = None
yL = None
xR = None
yR = None
filepath = None
heightOfVideo = None
widthOfVideo = None
methodOfRemoving = None
techniqueOfRemoving = None
counting_frames_given = None

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "a:b:c:d:e:f:g:h:i:j:")
    
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
        print("metoda odstranenia", methodOfRemoving); #0 all, 1 keras
    elif opt in ['-i']:
        techniqueOfRemoving = int(arg)  
        print("technika odstranenia", techniqueOfRemoving); #0 ns, 1 telea, 2 gauss, 3 median
    elif opt in ['-j']:
        counting_frames_given = int(arg)  
        print("Dane framy", counting_frames_given);
         
if(xL is None or yL is None or xR is None or yR is None or filepath is None or heightOfVideo is None or  widthOfVideo is None or methodOfRemoving is None or techniqueOfRemoving is None or counting_frames_given is None):
    print("dovidopo exitujeeme ,daco  je plano")
    sys.exit(1)


video = cv2.VideoCapture(filepath)
fpska = video.get(cv2.CAP_PROP_FPS) #pocet fps za sekundu


pipeline = keras_ocr.pipeline.Pipeline()
#f = open('output.txt','w') #zapisujem ake su titulky
poleObrazkov = []
fps_total = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #pocet framov celeho video
videocap = cv2.VideoCapture(filepath)
width_python = int(video.get(cv2.CAP_PROP_FRAME_WIDTH ))
height_python = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))



print("ZA MINUTU JE",fpska)
print("SPOLU JE",fps_total)


#fpska = video.get(cv2.CAP_PROP_FPS)
counting_frames = 0

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

kontola_ci_menim_masku = 1

mask = np.zeros((height_python,width_python,3),np.uint8) #vykreslenie ciernej masky v rozmeroch videa


output = cv2.VideoWriter(new_name_same_path, -1, fpska, (widthOfVideo,heightOfVideo)) #vysledne video

cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape

gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) #na premalovanie lebo inak sa to nevysvetlitelne stazuje
	

od_do_bool_stare = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
od_do_bool_nove = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
od_do_bool_stred = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
vsetky_titulky = []
kontrola_stare = 0
kontrola_nove = 0
suma_progressu_prva_cast = 0
suma_progressu_druha_cast = 700
suma_progressu_not_keras = 0
pocet_jednotiek = 0
progress_bar_first = 0
progress_bar_second = 0
progress_bar_third = 1000
progress_not_keras = 0
progress_less_than_950 = 0
progress_more_than_950 = 0
count_not_keras = 0



my_frequency_for_bar = 0


my_frequency_for_bar = fps_total / counting_frames_given
progress_bar_first = 700 / my_frequency_for_bar 

if (methodOfRemoving == 1):
    print("CAS_ODMAZANIA:",((fps_total//fpska)*12)//60)
else:
    print("CAS_ODMAZANIA:",((fps_total//fpska)*6)//60)
    sys.stdout.flush()


print("navysujeme pooo", progress_bar_first)


def medianblur(frame_s, maska): #method median blur
    medianblur_frame = cv2.medianBlur(frame_s, 71)
    mask3 = cv2.cvtColor(maska,cv2.COLOR_GRAY2RGB)#menime na 3farebnu
    normalized_mask3 = mask3.astype('float32') / 255.0
    #combined_image = np.zeros_like(frame_s)
    #combined_image.fill(255)
    a = np.multiply(1 - normalized_mask3, frame_s.astype('float32')) / 255.0
    b = np.multiply(normalized_mask3, medianblur_frame.astype('float32')) / 255.0
    no_subtitles_frame = np.add(a,b)
    no_subtitles_frame_uint8 = np.uint8(no_subtitles_frame * 255.0)  # Convert float32 to uint8
    return no_subtitles_frame_uint8

def gaussian(frame_s, maska): #method gaussian blur
    gauss_frame= cv2.GaussianBlur(frame_s, (151,151), 0) #blur povodny frame
    maska = cv2.GaussianBlur(maska, (5,5), 0) #blur masku
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilatedMask = cv2.dilate(maska, kernel, iterations=5) #dilatujeme aby bol usek kusok vasci
    mask3 = cv2.cvtColor(dilatedMask,cv2.COLOR_GRAY2RGB)#menime na 3farebnu
    normalized_mask3 = mask3.astype('float32') / 255.0
    #combined_image = np.zeros_like(frame_s)
    #combined_image.fill(255)
    a = np.multiply(1 - normalized_mask3, frame_s.astype('float32')) / 255.0
    b = np.multiply(normalized_mask3, gauss_frame.astype('float32')) / 255.0
    no_subtitles_frame = np.add(a,b)
    no_subtitles_frame_uint8 = np.uint8(no_subtitles_frame * 255.0)  # Convert float32 to uint8
    return no_subtitles_frame_uint8

def calculate_similarity(text1, text2):
    s = SequenceMatcher(None, text1, text2)
    similarity = s.ratio()
    return similarity

def zero_frame(titulky_start): #zamazem celu oblast lebo začinaju titulky na nultej snimke už hned
    mask = np.zeros((height_python,width_python,3),np.uint8) #vykreslenie ciernej masky v rozmeroch videa
    cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape
    zakladna_maska = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) #na premalovanie lebo inak sa to nevysvetlitelne stazuje
    return zakladna_maska

def not_zero_frame(titulky_start):
    zakladna_maska = np.zeros((height_python,width_python),np.uint8) #vykreslenie ciernej masky v rozmeroch videa
    bez_tituliek = titulky_start - 1
    videocap.set(cv2.CAP_PROP_POS_FRAMES, (titulky_start + 1)) #preistotu plus 1 frame
    ret, img_titulky = videocap.read()
    img_titulky = img_titulky[yL:yR,xL:xR]
    img_titulky_gray = cv2.cvtColor(img_titulky, cv2.COLOR_BGR2GRAY)   #oblast s titulkami v ciernobielej
    #cv2.imwrite('img_titu.jpg', img_titulky_gray)

    videocap.set(cv2.CAP_PROP_POS_FRAMES, bez_tituliek)
    ret, img_bez = videocap.read()
    img_bez = img_bez[yL:yR,xL:xR]
    img_bez_gray = cv2.cvtColor(img_bez, cv2.COLOR_BGR2GRAY) #oblast snimky pred danou snimkou v ciermnobielej
    #cv2.imwrite('img_bez.jpg', img_bez_gray)

    img_subtract = cv2.absdiff(img_titulky_gray, img_bez_gray) #odcitanie
    #cv2.imwrite('img_subst.jpg', img_subtract)

    ret, thresh = cv2.threshold(img_subtract,50, 255, cv2.THRESH_BINARY) #theshold

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    #toto je vlastne ta mala orezana maska na titulky
    dilated = cv2.dilate(thresh, kernel, iterations=2) #dilatacia na vyplnenie bielych medziet    
    rows, cols = dilated.shape
    channels = 1 #je ciernobiela

    print(zakladna_maska[yL:yL+rows, xL:xL+cols].shape)
    print(dilated.shape)

    zakladna_maska[yL:yL+rows, xL:xL+cols] = cv2.addWeighted(zakladna_maska[yL:yL+rows, xL:xL+cols], 0, dilated, 1, 0)

    return zakladna_maska
    #dilated_gray = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY) #neoribm lebo snimka uz je ciernobiela

    #davam malu oblast spat do velkej masky

def create_mask(titulky_start):

    #print("PROGRESS: 555")
    global suma_progressu_druha_cast
    global progress_bar_second
    suma_progressu_druha_cast += progress_bar_second
    print("PROGRESS: ",int(suma_progressu_druha_cast))
    print("KONTROLKA", titulky_start)
    sys.stdout.flush()

    if titulky_start != 0:
        zakladna_maska = not_zero_frame(titulky_start)
    else: 
        zakladna_maska = zero_frame(titulky_start)

    return zakladna_maska

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
    print(particular_text, "frame", frame_number)
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
        similarity = calculate_similarity(text, end_text)
        
        '''if text is None:
            podobnost_vlastna = 0.41
        elif len(text) <= 4:
            podobnost_vlastna = 0.41
        else:
            podobnost_vlastna = 0.41'''
        if similarity < 0.39:
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
        similarity = calculate_similarity(text, start_text)

        '''if text is None:
            podobnost_vlastna = 0.41
        elif len(text) <= 4:
            podobnost_vlastna = 0.41
        else:
            podobnost_vlastna = 0.41'''

        if similarity < 0.39:
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

    od_do_bool_stare[1] += 1 #extraframe preisottu
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
            #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file 
            poleObrazkov.append(image)
            #print(poleObrazkov)
            cislo_frame += counting_frames_given #cca 30framov ma sekunda
            videocap.set(cv2.CAP_PROP_POS_FRAMES, cislo_frame)
            success,image = videocap.read()
        else:
            images = [keras_ocr.tools.read(img) for img in poleObrazkov]
            prediction_groups = pipeline.recognize(images)
            for x in range(len(images)):
                #with open('output.txt', 'a') as f:
                    #print("",file=f)
                    #print("FRAME",counting_frames,"Z", fps_total, file=f)
                counting_frames = counting_frames + counting_frames_given
                suma_progressu_prva_cast += progress_bar_first
                print("PROGRESS: ",int(suma_progressu_prva_cast))
                sys.stdout.flush()
                for text, box in prediction_groups[x]:
                    text_aktual.append(text)
                    #with open('output.txt', 'a') as f:
                        #print(text, file=f)

                s = SequenceMatcher(None, text_aktual, text_predch)
                similarity = s.ratio()

                if((counting_frames-counting_frames_given) != 0):
                    
                    print((counting_frames -(counting_frames_given*2))," je",text_predch,"a", (counting_frames - counting_frames_given), "je", text_aktual)
                    if similarity >= 0.4:
                        print("Text sa zhoduje alebo je veľmi podobný.")
                        od_do_bool_stare[1]=(counting_frames - counting_frames_given)
                    else:
                        print("Text sa nezhoduje.")
                        prvy_frame = counting_frames - (counting_frames_given*2)
                        druhy_frame = counting_frames - counting_frames_given

                        od_do_bool_stare[1]=(counting_frames - (counting_frames_given*2))
                        od_do_bool_nove[1]=(counting_frames - counting_frames_given)

                        find_exact_frame(prvy_frame,druhy_frame,text_predch,text_aktual)#VOLAME FUNKCIU NA BISEKCIU

                    text_predch = text_aktual
                    text_aktual = []
                else:
                    od_do_bool_stare[0]=0
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
            #with open('output.txt', 'a') as f:
                #print("",file=f)
                #print("FRAME",counting_frames,"Z", fps_total, file=f)
            counting_frames = counting_frames + counting_frames_given
            suma_progressu_prva_cast += progress_bar_first
            print("PROGRESS: ",int(suma_progressu_prva_cast))
            sys.stdout.flush()
            for text, box in prediction_groups[x]:
                text_aktual.append(text)
                #with open('output.txt', 'a') as f:
                    #print(text, file=f)

            s = SequenceMatcher(None, text_aktual, text_predch)
            similarity = s.ratio()

            if((counting_frames-counting_frames_given) != 0):
                print((counting_frames -(counting_frames_given*2))," je",text_predch,"a", (counting_frames - counting_frames_given), "je", text_aktual)
                if similarity >= 0.4:
                    print("Text sa zhoduje alebo je veľmi podobný.")
                    od_do_bool_stare[1]=(counting_frames - counting_frames_given)
                else:
                    print("Text sa nezhoduje.")
                    prvy_frame = counting_frames - (counting_frames_given*2)
                    druhy_frame = counting_frames - counting_frames_given

                    od_do_bool_stare[1]=(counting_frames - (counting_frames_given*2))
                    od_do_bool_nove[1]=(counting_frames - counting_frames_given)

                    find_exact_frame(prvy_frame,druhy_frame,text_predch,text_aktual)

                text_predch = text_aktual
                text_aktual = []
            else:
                od_do_bool_stare[0]=0
                text_predch = text_aktual
                text_aktual = []

    od_do_bool_stare[1]=fps_total-1 #pocetframov
    od_do_bool_stare[1] += 1 #extraframe preisottu
    vsetky_titulky.append(od_do_bool_stare[:])
    print("vsetky",vsetky_titulky)
    pocet_jednotiek = len([lst for lst in vsetky_titulky if lst[-1] == 1])
    print(pocet_jednotiek)
    progress_bar_second = 250 / pocet_jednotiek



if (video.isOpened()== False): 
    print("Error opening video file")

while(video.isOpened()):
    if methodOfRemoving == 0:
        ret, frame = video.read()
        count_not_keras+=1
        # Capture frame-by-frame
        if ret == True:
            # Press Q on keyboard to  exit
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
            #print("KONTRPOLA")
            if(count_not_keras == 1 and fps_total < 950):
                progress_less_than_950 = fps_total/950
                everyframeislike = 1//progress_less_than_950
                chceme_kazdych = everyframeislike*10
                pomocna_suma = chceme_kazdych

            elif (count_not_keras == 1 and fps_total > 950):
                everyframeislike = fps_total//950
                chceme_kazdych = everyframeislike*10
                pomocna_suma = chceme_kazdych

            print("count", count_not_keras,"pomoc",pomocna_suma)
            sys.stdout.flush()

            if (count_not_keras ==pomocna_suma):
                budeme_opakovat = 950//(fps_total//chceme_kazdych)
                suma_progressu_not_keras += budeme_opakovat
                print("PROGRESS: ",suma_progressu_not_keras)
                print("pred",pomocna_suma)
                pomocna_suma+=chceme_kazdych
                print("po",pomocna_suma)
                sys.stdout.flush()

            
            if techniqueOfRemoving == 0: #inpaiting NS vsetko
                no_subtitles_frame = cv2.inpaint(frame,gray_mask,3,cv2.INPAINT_NS) #pomocou inpaint odstranujem (iba zamazavam) titulky
                output.write(no_subtitles_frame)
            elif techniqueOfRemoving == 1: #inpaiting TELEA vsetko
                no_subtitles_frame = cv2.inpaint(frame,gray_mask,3,cv2.INPAINT_TELEA) #pomocou inpaint odstranujem (iba zamazavam) titulky
                output.write(no_subtitles_frame)
            elif techniqueOfRemoving == 2: #gauss vsetko
                no_subtitles_frame = gaussian(frame,gray_mask)
                output.write(no_subtitles_frame)
            elif techniqueOfRemoving == 3: #median blue vsetko
                no_subtitles_frame = medianblur(frame,gray_mask)
                output.write(no_subtitles_frame)
        else: 
            break
        #video.release()
    else: #method of remov je 1, teda keras 
        ret, frame = video.read()
       
        if ret == True:
            # Get the current frame number
            frame_number = int(video.get(cv2.CAP_PROP_POS_FRAMES)) - 1
            #print(frame_number)

            # Loop through the title ranges to see if the current frame is within a title range
            found_title_range = False
            for i, (title_start, title_end, title_bool) in enumerate(vsetky_titulky):
                if title_bool == 1 and frame_number == title_start:
                    presna_maska = create_mask(frame_number)
                if frame_number >= title_start and frame_number <= title_end and title_bool == 1:
                    found_title_range = True
                                
                if i < len(vsetky_titulky)-1 and title_bool == 1 and vsetky_titulky[i+1][2] == 1:
                    next_title_start, _, _ = vsetky_titulky[i+1]
                    if frame_number == title_end and next_title_start != title_end:
                        presna_maska = create_mask(frame_number)
                        found_title_range = False # reset flag to ensure that the current frame is not written to the output
                        continue # skip writing the current frame to the output
                    
            # Check if the current frame is within the last subtitle range and if that range has bool 1
            last_title_start, last_title_end, last_title_bool = vsetky_titulky[-1]
            if frame_number >= last_title_start and frame_number <= last_title_end and last_title_bool == 1:
                found_title_range = True
                if last_title_bool == 1 and frame_number == last_title_start:
                    presna_maska = create_mask(frame_number)
            
            # If the current frame is not within a title range, write it to the output with no modifications
            #frame nemenimne nijak
            if not found_title_range: #bez tituliek
                output.write(frame)
                #kontola_ci_menim_masku = 1
            # If the current frame is within a title range, modify it as needed
            else:
                #if kontola_ci_menim_masku == 1: #menim masku
                   # presna_maska = create_mask(frame_number)
                    #kontola_ci_menim_masku = 0
                
                if techniqueOfRemoving == 0: #inpaiting NS
                    no_subtitles_frame = cv2.inpaint(frame,presna_maska,3,cv2.INPAINT_NS)
                    output.write(no_subtitles_frame)
                
                elif techniqueOfRemoving == 1: #inpaiting telea
                    no_subtitles_frame = cv2.inpaint(frame,presna_maska,3,cv2.INPAINT_TELEA)
                    output.write(no_subtitles_frame)
                    
                elif techniqueOfRemoving == 2: #gauss
                    #print("TU SOM")
                    no_subtitles_frame = gaussian(frame,presna_maska)
                    output.write(no_subtitles_frame)
                elif techniqueOfRemoving == 3: #median blur vsetko
                    no_subtitles_frame = medianblur(frame,presna_maska)
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
print("PROGRESS: 951")
sys.stdout.flush()
audio_clip = AudioFileClip(filepath)   #audio ziskavam lebo cv2 nepouziva
modified_clip = VideoFileClip(new_name_same_path)
final_clip = modified_clip.set_audio(audio_clip)
final_clip.write_videofile(new_name_same_path1)
os.remove(new_name_same_path)


print("Video has been released.")
print("PROGRESS: ",progress_bar_third)
casik = 0
casik = str(datetime.timedelta(seconds=(time.time() - start_time)))
print("Removing subtitles took",casik)
