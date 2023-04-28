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

od_do_bool_stare = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
od_do_bool_nove = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
od_do_bool_stred = [0,0,0] #0 neodmazavam (prazdy text), 1 odmazavam (su tam titulky)
vsetky_titulky = []
kontrola_stare = 0
kontrola_nove = 0



def text_on_particular_frame(frame_number):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    prediction_groups_bis = []
    success, image = video.read()

    if not success:
        return
    
    image = image[dolna_tretina_vyska:height,prva_desatina_sirky:posledna_desatina_sirky]
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

        if len(text) <= 4:
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

        if len(text) <= 4:
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
                print((counting_frames -60)," je",text_predch,"a", (counting_frames - 30), "je", text_aktual)
                if similarity >= 0.5:
                    print("Text sa zhoduje alebo je veľmi podobný.")
                    od_do_bool_stare[1]=(counting_frames - 30)
                else:
                    print("Text sa nezhoduje.")
                    prvy_frame = counting_frames - 60
                    druhy_frame = counting_frames - 30

                    od_do_bool_stare[1]=(counting_frames - 60)
                    od_do_bool_nove[1]=(counting_frames - 30)
                    
                    #volame funkciu
                    find_exact_frame(prvy_frame,druhy_frame,text_predch,text_aktual)

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
            if similarity >= 0.5:
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

od_do_bool_stare[1]=fpska-1 #pocetframov
vsetky_titulky.append(od_do_bool_stare[:])
print("vsetky",vsetky_titulky)


