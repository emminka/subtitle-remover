######################
# Emma Krompascikova #
# Bachelor Thesis    #
# Hardsub Remover    #
# May 2023           #
######################

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
height_of_video = None
width_of_video = None
method_of_removing = None
technique_of_removing = None
counting_frames_given = None

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "a:b:c:d:e:f:g:h:i:j:")
    
except:
    print("Error")

for opt, arg in opts:
    if opt in ['-a']:
        xL = int(arg)
    elif opt in ['-b']:
        yL = int(arg)
    elif opt in ['-c']:
        xR = int(arg)
    elif opt in ['-d']:
        yR = int(arg)  
    elif opt in ['-e']:
        filepath = arg  
    elif opt in ['-f']:
        height_of_video = int(arg)
    elif opt in ['-g']:
        width_of_video = int(arg)  
    elif opt in ['-h']:
        method_of_removing = int(arg)  #0 all, 1 keras
    elif opt in ['-i']:
        technique_of_removing = int(arg)   #0 ns, 1 telea, 2 gauss, 3 median
    elif opt in ['-j']:
        counting_frames_given = int(arg)  
         
if(xL is None or yL is None or xR is None or yR is None or filepath is None or height_of_video is None or  width_of_video is None or method_of_removing is None or technique_of_removing is None or counting_frames_given is None):
    print("Error. There is an argument which in None.")
    sys.exit(1)


video = cv2.VideoCapture(filepath)
fps_second = video.get(cv2.CAP_PROP_FPS) #frames per second

pipeline = keras_ocr.pipeline.Pipeline()
array_of_frames = []
fps_total = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #frames in the whole video
videocap = cv2.VideoCapture(filepath)
width_python = int(video.get(cv2.CAP_PROP_FRAME_WIDTH ))
height_python = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Frames per second",fps_second)
print("Frames total",fps_total)

counting_frames = 0
count = 0
number_of_frame = 1
images = []
text_actual = []
text_before = []

suffix = "_noSUB_noSOUND.mp4"
new_name_same_path = filepath.rsplit(".", 1)[0];
new_name_same_path += suffix;

suffix_final = "_noSUB_yesSOUND.mp4"
new_name_same_path_final = filepath.rsplit(".", 1)[0];
new_name_same_path_final += suffix_final;
print(new_name_same_path_path)

mask = np.zeros((height_python,width_python,3),np.uint8) #make black mask in size of video
output = cv2.VideoWriter(new_name_same_path, -1, fps_second, (width_of_video,height_of_video)) #final video
cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape, draw white box for mask
gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) #changing chanels

#index 0 - from, index 1 to, index 2 - zero is not removing, 1 is removing	
info_subtitles_old = [0,0,0] 
info_subtitles_new = [0,0,0] 
info_subtitles_middle = [0,0,0]

all_info_subtitles = []
checking_old = 0
checking_new = 0
sum_progress_first = 0
sum_progressu_second = 700
suma_progressu_not_keras = 0
sum_of_ones = 0
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

if (method_of_removing == 1):
    print("TIME_OF_REMOVING:",((fps_total//fps_second)*12)//60)
else:
    print("TIME_OF_REMOVING:",((fps_total//fps_second)*6)//60)
    sys.stdout.flush()

def medianblur(frame_s, maska): #method median blur
    medianblur_frame = cv2.medianBlur(frame_s, 71)
    mask3 = cv2.cvtColor(maska,cv2.COLOR_GRAY2RGB)#changing to 3 colors
    normalized_mask3 = mask3.astype('float32') / 255.0
    a = np.multiply(1 - normalized_mask3, frame_s.astype('float32')) / 255.0
    b = np.multiply(normalized_mask3, medianblur_frame.astype('float32')) / 255.0
    no_subtitles_frame = np.add(a,b)
    no_subtitles_frame_uint8 = np.uint8(no_subtitles_frame * 255.0)  # convert float32 to uint8
    return no_subtitles_frame_uint8

def gaussian(frame_s, maska): #method gaussian blur
    gauss_frame= cv2.GaussianBlur(frame_s, (151,151), 0) #blur original frame
    maska = cv2.GaussianBlur(maska, (5,5), 0) #blur masku
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilatedMask = cv2.dilate(maska, kernel, iterations=5) #dilatatiton for bigger area
    mask3 = cv2.cvtColor(dilatedMask,cv2.COLOR_GRAY2RGB)#changing to 3 colors
    normalized_mask3 = mask3.astype('float32') / 255.0
    a = np.multiply(1 - normalized_mask3, frame_s.astype('float32')) / 255.0
    b = np.multiply(normalized_mask3, gauss_frame.astype('float32')) / 255.0
    no_subtitles_frame = np.add(a,b)
    no_subtitles_frame_uint8 = np.uint8(no_subtitles_frame * 255.0)  # convert float32 to uint8
    return no_subtitles_frame_uint8

def calculate_similarity(text1, text2):
    s = SequenceMatcher(None, text1, text2)
    similarity = s.ratio()
    return similarity

def zero_frame(subtitles_start): #delete whole area becasue subt. are starting on first frame
    mask = np.zeros((height_python,width_python,3),np.uint8) #black mask in video size
    cv2.rectangle(mask, (xL, yL), (xR, yR),(255,255,255), -1) #-1 for filled shape, draw white rectangle
    primary_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) #2 chanells
    return primary_mask

def not_zero_frame(subtitles_start):
    primary_mask = np.zeros((height_python,width_python),np.uint8) #black mask in video size
    no_subtitles = subtitles_start - 1
    videocap.set(cv2.CAP_PROP_POS_FRAMES, (subtitles_start + 1)) #just in case use extra frame
    ret, image_for_subtitles = videocap.read()
    image_for_subtitles = image_for_subtitles[yL:yR,xL:xR] #crop to the chosen area
    image_for_subtitles_gray = cv2.cvtColor(image_for_subtitles, cv2.COLOR_BGR2GRAY)
    videocap.set(cv2.CAP_PROP_POS_FRAMES, no_subtitles)
    ret, image_without_subtitles = videocap.read()
    image_without_subtitles = image_without_subtitles[yL:yR,xL:xR]
    image_without_subtitles_gray = cv2.cvtColor(image_without_subtitles, cv2.COLOR_BGR2GRAY) #area of frame before given frame

    img_subtract = cv2.absdiff(image_for_subtitles_gray, image_without_subtitles_gray) #absulote difference
    ret, thresh = cv2.threshold(img_subtract,50, 255, cv2.THRESH_BINARY) #theshold
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    dilated = cv2.dilate(thresh, kernel, iterations=2) #dilatation for filling space
    rows, cols = dilated.shape
    primary_mask[yL:yL+rows, xL:xL+cols] = cv2.addWeighted(primary_mask[yL:yL+rows, xL:xL+cols], 0, dilated, 1, 0)#put masks together
    return primary_mask

def create_mask(subtitles_start):
    global sum_progressu_second
    global progress_bar_second
    sum_progressu_second += progress_bar_second
    print("PROGRESS: ",int(sum_progressu_second))
    print("creating mask on frame", subtitles_start)
    sys.stdout.flush()

    if subtitles_start != 0:
        primary_mask = not_zero_frame(subtitles_start)
    else: 
        primary_mask = zero_frame(subtitles_start)

    return primary_mask

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
    return particular_text

def find_exact_frame(start_frame,end_frame,start_text,end_text): #bisection
    global info_subtitles_new
    global info_subtitles_old
    global info_subtitles_middle
    global checking_new
    global checking_old

    print("starting frame is", start_frame)
    print("ending frame is", end_frame)
    low_frame = start_frame
    high_frame = end_frame
    middle_frame = 0
    while low_frame < high_frame:    
        middle_frame = (low_frame + high_frame) // 2 #calculate the middle frame
        text = text_on_particular_frame(middle_frame)
        similarity = calculate_similarity(text, end_text)

        if similarity < 0.39:#text does not match, update the search range by +1
            low_frame = middle_frame + 1
        else:#text matches, update the search range
            high_frame = middle_frame
            if (text == []):
                info_subtitles_new[2]=0 #not removing
            else:
                info_subtitles_new[2]=1 #removing
            
    print('End text starts at', high_frame)
    info_subtitles_new[0]=high_frame
    checking_new=high_frame

    #define the search range using the found frame and the end frame
    second_subsubtitle_from = high_frame
    low_frame = start_frame
    high_frame = second_subsubtitle_from

    while low_frame < high_frame:       
        middle_frame = (low_frame + high_frame) // 2 #calculate the middle frame
        text = text_on_particular_frame(middle_frame)
        similarity = calculate_similarity(text, start_text)#calculate similarity between extracted text and the start text
        if similarity < 0.39:
            high_frame = middle_frame#text does not match, update the search range
        else:
            low_frame = middle_frame + 1#text matches, update the search range
            if (text == []):
                info_subtitles_old[2]=0 #not removing
            else:
                info_subtitles_old[2]=1 #removing

    print('first subt start at', low_frame - 1)
    info_subtitles_old[1]=(low_frame - 1)
    checking_old=(low_frame - 1)

    info_subtitles_old[1] += 1 #extraframe just in case
    all_info_subtitles.append(info_subtitles_old[:])
    info_subtitles_old = info_subtitles_new
    info_subtitles_new=[0,0,0]

    if(checking_old+1 != checking_new):
        info_subtitles_middle[0]=checking_old+1
        info_subtitles_middle[1]=checking_new-1
        all_info_subtitles.append(info_subtitles_middle[:])
        info_subtitles_middle=[0,0,0]

if method_of_removing == 1: #using keras, Subtitle Only method
    success,image = videocap.read()
    while success:
        if(count<8):
            image = image[yL:yR,xL:xR]  #cropped image, from:to and from:to
            array_of_frames.append(image)
            number_of_frame += counting_frames_given #default is 30
            videocap.set(cv2.CAP_PROP_POS_FRAMES, number_of_frame)
            success,image = videocap.read()
        else:
            images = [keras_ocr.tools.read(img) for img in array_of_frames]
            prediction_groups = pipeline.recognize(images)
            for x in range(len(images)):
                counting_frames = counting_frames + counting_frames_given
                sum_progress_first += progress_bar_first
                print("PROGRESS: ",int(sum_progress_first))
                sys.stdout.flush()
                for text, box in prediction_groups[x]:
                    text_actual.append(text)
                s = SequenceMatcher(None, text_actual, text_before)
                similarity = s.ratio()
                if((counting_frames-counting_frames_given) != 0):
                    if similarity >= 0.39: #text is same or very similiar
                        info_subtitles_old[1]=(counting_frames - counting_frames_given)
                    else:#text is different
                        first_frame = counting_frames - (counting_frames_given*2)
                        second_frame = counting_frames - counting_frames_given
                        info_subtitles_old[1]=(counting_frames - (counting_frames_given*2))
                        info_subtitles_new[1]=(counting_frames - counting_frames_given)
                        find_exact_frame(first_frame,second_frame,text_before,text_actual)#calling bisection function
                    text_before = text_actual
                    text_actual = []
                else:
                    info_subtitles_old[0]=0
                    text_before = text_actual
                    text_actual = []
            count = -1
            array_of_frames = []
            images = []
            prediction_groups = []
        count += 1
    if not array_of_frames:
        print("Nothing in array of frames")
    else:
        images = [keras_ocr.tools.read(img) for img in array_of_frames]
        prediction_groups = pipeline.recognize(images)
        for x in range(len(images)):
            counting_frames = counting_frames + counting_frames_given
            sum_progress_first += progress_bar_first
            print("PROGRESS: ",int(sum_progress_first))
            sys.stdout.flush()
            for text, box in prediction_groups[x]:
                text_actual.append(text)
            s = SequenceMatcher(None, text_actual, text_before)
            similarity = s.ratio()

            if((counting_frames-counting_frames_given) != 0):
                print((counting_frames -(counting_frames_given*2))," je",text_before,"a", (counting_frames - counting_frames_given), "je", text_actual)
                if similarity >= 0.39:#text is same or very similiar
                    info_subtitles_old[1]=(counting_frames - counting_frames_given)
                else:#text not same
                    first_frame = counting_frames - (counting_frames_given*2)
                    second_frame = counting_frames - counting_frames_given
                    info_subtitles_old[1]=(counting_frames - (counting_frames_given*2))
                    info_subtitles_new[1]=(counting_frames - counting_frames_given)
                    find_exact_frame(first_frame,second_frame,text_before,text_actual)
                text_before = text_actual
                text_actual = []
            else:
                info_subtitles_old[0]=0
                text_before = text_actual
                text_actual = []

    info_subtitles_old[1]=fps_total-1 #number of frames
    info_subtitles_old[1] += 1 #extraframe just in case
    all_info_subtitles.append(info_subtitles_old[:])
    print("all",all_info_subtitles)
    sum_of_ones = len([lst for lst in all_info_subtitles if lst[-1] == 1]) #the total number of different subtitles
    print(sum_of_ones)
    progress_bar_second = 250 / sum_of_ones

if (video.isOpened()== False): 
    print("Error opening video file")

while(video.isOpened()):
    if method_of_removing == 0: #method remove all
        ret, frame = video.read()
        count_not_keras+=1
        if ret == True:  
            if(count_not_keras == 1 and fps_total < 950):
                progress_less_than_950 = fps_total/950
                every_frame_is_like = 1//progress_less_than_950
                wanted_every_x_frame = every_frame_is_like*10
                helping_sum = wanted_every_x_frame
            elif (count_not_keras == 1 and fps_total > 950):
                every_frame_is_like = fps_total//950
                wanted_every_x_frame = every_frame_is_like*10
                helping_sum = wanted_every_x_frame
            sys.stdout.flush()

            if (count_not_keras ==helping_sum):
                budeme_opakovat = 950//(fps_total//wanted_every_x_frame)
                suma_progressu_not_keras += budeme_opakovat
                print("PROGRESS: ",suma_progressu_not_keras)
                helping_sum+=wanted_every_x_frame
                sys.stdout.flush()
            if technique_of_removing == 0: #inpaiting ns all
                no_subtitles_frame = cv2.inpaint(frame,gray_mask,3,cv2.INPAINT_NS)
                output.write(no_subtitles_frame)
            elif technique_of_removing == 1: #inpaiting telea all
                no_subtitles_frame = cv2.inpaint(frame,gray_mask,3,cv2.INPAINT_TELEA)
                output.write(no_subtitles_frame)
            elif technique_of_removing == 2: #gauss all
                no_subtitles_frame = gaussian(frame,gray_mask)
                output.write(no_subtitles_frame)
            elif technique_of_removing == 3: #median all
                no_subtitles_frame = medianblur(frame,gray_mask)
                output.write(no_subtitles_frame)
        else: 
            break
    else: #method of remov is 1, subtitle only 
        ret, frame = video.read() 
        if ret == True:      
            frame_number = int(video.get(cv2.CAP_PROP_POS_FRAMES)) - 1 #get current frame number
            #going through subtitle ranges to see if the current frame is within a subtitle range
            found_subtitle_range = False
            for i, (subtitle_from, subtitle_until, subtitle_bool) in enumerate(all_info_subtitles):
                if subtitle_bool == 1 and frame_number == subtitle_from:
                    presna_maska = create_mask(frame_number)
                if frame_number >= subtitle_from and frame_number <= subtitle_until and subtitle_bool == 1:
                    found_subtitle_range = True
                                
                if i < len(all_info_subtitles)-1 and subtitle_bool == 1 and all_info_subtitles[i+1][2] == 1:
                    next_subtitle_from, _, _ = all_info_subtitles[i+1]
                    if frame_number == subtitle_until and next_subtitle_from != subtitle_until:
                        presna_maska = create_mask(frame_number)
                        found_subtitle_range = False # reset flag to ensure that the current frame is not written to the output
                        continue # skip writing the current frame to the output
                    
            #check if the current frame is within the last subtitle range and if that range has bool 1
            last_subtitle_from, last_subtitle_until, last_subtitle_bool = all_info_subtitles[-1]
            if frame_number >= last_subtitle_from and frame_number <= last_subtitle_until and last_subtitle_bool == 1:
                found_subtitle_range = True
                if last_subtitle_bool == 1 and frame_number == last_subtitle_from:
                    presna_maska = create_mask(frame_number)
            

            if not found_subtitle_range: #no subtitles, not changing frame
                output.write(frame)
                if technique_of_removing == 0: #inpaiting NS
                    no_subtitles_frame = cv2.inpaint(frame,presna_maska,3,cv2.INPAINT_NS)
                    output.write(no_subtitles_frame)
                elif technique_of_removing == 1: #inpaiting telea
                    no_subtitles_frame = cv2.inpaint(frame,presna_maska,3,cv2.INPAINT_TELEA)
                    output.write(no_subtitles_frame)
                elif technique_of_removing == 2: #gauss
                    no_subtitles_frame = gaussian(frame,presna_maska)
                    output.write(no_subtitles_frame)
                elif technique_of_removing == 3: #median
                    no_subtitles_frame = medianblur(frame,presna_maska)
                    output.write(no_subtitles_frame)
                if len(all_info_subtitles) > 1:#check if next frame is in range following with bool of rmeoving
                    next_subtitle_from, next_subtitle_until, next_subtitle_bool = all_info_subtitles[1]
                    if frame_number == subtitle_until and next_subtitle_bool == 0:
                        video.read() # skip the next frame
        else:
            break

output.release()
print("PROGRESS: 951")
sys.stdout.flush()
audio_clip = AudioFileClip(filepath)   #getting audio from original
modified_clip = VideoFileClip(new_name_same_path) 
final_clip = modified_clip.set_audio(audio_clip)
final_clip.write_videofile(new_name_same_path_final)
os.remove(new_name_same_path)

print("Video has been released.")
print("PROGRESS: ",progress_bar_third)
final_time = 0
final_time = str(datetime.timedelta(seconds=(time.time() - start_time)))
print("Removing subtitles took",final_time)
