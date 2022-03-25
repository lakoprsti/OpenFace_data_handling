import pandas as pd
from moviepy.editor import *
from multiprocessing import Process, Semaphore
import csv 

####This code is written by Ana Marinic#####
#NOTE: if the files are not saved in the same folder as the programme you must include the path to the files!!!



def makeData():
    data = pd.read_csv('PA01A.csv') ################add name of the file here#################
    au06 = list(data[' AU06_c'])
    au12 = list(data[' AU12_c'])
    eye_gaze_horizontal = list(data[' gaze_angle_x'])
    eye_gaze_vertical = list(data[' gaze_angle_y'])
    smilestarts = startsmile(au06,au12)
    with open("optput_eye_gaze.txt", "w") as o: ###############CREATE and NAME the output file here####################
        print("smiles.starts:", smilestarts, len(smilestarts), file=o)
    smileends = endsmile(au06,au12)
    with open("optput_eye_gaze.txt", "a") as o:
        print("smiles.ends:",smileends, len(smileends), file=o)
    return(smilestarts, smileends, eye_gaze_horizontal, eye_gaze_vertical)

def eyeGazeLocations():
    Df = pd.read_csv('PA01A.csv') ########################add name of the file here#####################
    eye_gaze_horizontal = list(Df[' gaze_angle_x'])
    eye_gaze_vertical = list(Df[' gaze_angle_y']) 
    return(eye_gaze_horizontal, eye_gaze_vertical)

####gaze calibration stuff#####
  
def gazecalibration(second_smile): 
    column1, column2 = eyeGazeLocations()
    print("starting the function gazecalibration now")
    a, b  = max(column1), min(column1)  ##horizontal maximum and minimum
    with open("optput_eye_gaze.txt", "a") as o:
        print("horizontal maximum and minimum: ", a, b, file=o)
    c, d = max(column2), min(column2) ##vertical maximum and minium
    with open("optput_eye_gaze.txt", "a") as o:
        print("vertical maximum and minium: ", c, d, file=o)
    d = (a+b)/2  ##origin value horizontal
    e = (c+d)/2  ##origin value vertical
    with open("optput_eye_gaze.txt", "a") as o:
        print("origin point - centre of the screen: ", d, e, file=o)
    frames_when_they_look, looking_out, which_corner_is_it = looking_person_values (column1, column2, a, b, c, d, second_smile) ##loking at the person value 
    with open("optput_eye_gaze.txt", "a") as o:
        print("this is the corner where the other person is:", str(which_corner_is_it[0]), file=o)
        print("1 = bottom right\n2 = top right\n3 = top left\n4 = bottom left", file=o)
    return(a, b, c, d, which_corner_is_it)

def looking_person_values (column1, column2, a, b, c, d, second_smile): ##get the values which would be indicative of the participants looking at the other person: if they look outside of the 4 corners of the picture #####column 1 = horizontal column2 = vertical### to call: looking_person_values (column1, column2, a, b, c, d)
    print("starting the function looking_person_values now")
    looking_out = []
    frames_when_they_look = []
    horizontal_tolerance = (abs(a)+abs(b))*0.15
    vertical_tolerance = (abs(c)+abs(d))*0.15
    which_corner_is_it = []
    for i in range (0, second_smile):   
        if (column1[i]> a-horizontal_tolerance and column2[i]>c-vertical_tolerance):
            frames_when_they_look +=[i]
            looking_out +=[(column1, column2)] 
            which_corner_is_it =[1] #bottom left
        elif (column1[i] < b+horizontal_tolerance and column2[i]>c-vertical_tolerance):
            frames_when_they_look +=[i]
            looking_out +=[(column1, column2)] 
            which_corner_is_it =[2] #bottom right
        elif (column1[i]<b+horizontal_tolerance and column2[i]<d+vertical_tolerance):
            frames_when_they_look +=[i]
            looking_out +=[(column1, column2)]
            which_corner_is_it =[3] #top right
        elif (column1[i]> a-horizontal_tolerance and column2[i]<d+vertical_tolerance):
            frames_when_they_look +=[i]
            looking_out +=[(column1, column2)]
            which_corner_is_it =[4] #top left
    return(frames_when_they_look, looking_out, which_corner_is_it)

def find_all_smiles(column1, column2, a, b, c, d, which_corner_is_it):
    print("starting the function find_all_smiles now")
    print(len(column1))
    looking_out = []
    frames_when_they_look = []
    horizontal_tolerance = (abs(a)+abs(b)) *0.20
    vertical_tolerance = (abs(c)+abs(d)) *0.20
    if which_corner_is_it[0] == 1: 
        for i in range(len(column1)): 
            if (column1[i]> a-horizontal_tolerance and column2[i]>c-vertical_tolerance):
                frames_when_they_look +=[i]
                looking_out +=[(column1, column2)]   
    elif which_corner_is_it[0] == 2:
        for i in range(len(column1)):
            if (column1[i] < b+horizontal_tolerance and column2[i]>c-vertical_tolerance):
                frames_when_they_look +=[i]
                looking_out +=[(column1, column2)] 
    elif which_corner_is_it[0] == 3:
        for i in range(len(column1)):
            if (column1[i]<b+horizontal_tolerance and column2[i]<d+vertical_tolerance):
                frames_when_they_look +=[i]
                looking_out +=[(column1, column2)] 
    elif which_corner_is_it[0] == 4:
        for i in range(len(column1)):
            if (column1[i]> a-horizontal_tolerance and column2[i]<d+vertical_tolerance):
                frames_when_they_look +=[i]
                looking_out +=[(column1, column2)]
    return(frames_when_they_look)

def gaze_by_condition(frames_when_they_look, first_smile):
    relevant_gazes = frames_when_they_look[first_smile:]
    condition1=[]
    condition2=[]
    condition3=[]
    for e in relevant_gazes:
        if e <(len(frames_when_they_look)/3):
            condition1+=[e]
        elif e > (len(frames_when_they_look)/3) and e < ((len(frames_when_they_look)/3)*2):
            condition2+=[e]
        else:
            condition3+=[e]

    with open("optput_eye_gaze.txt", "a") as o:
        print("all of the frames when participants looks at the other person:", frames_when_they_look, file = o)
        print ("condition 1:", condition1, file=o)
        print("duration of the looking in condition 1:", len(condition1)*10/100, file=o)
        print ("condition 2:", condition2, file= o)
        print("duration of the looking in condition 2:", len(condition2)*10/100, file=o)
        print ("condition 3:", condition3, file = o)
        print("duration of the looking in condition 3:", len(condition3)*10/100, file=o)
        o.close()


####end of gaze stuff#####

def startsmile(column1, column2):  
    a = [] 
    for i in range (1, len(column1)):
         if ((float(column1[i-1])) == 0 and (float(column2[i-1])) == 0) and ((float(column1[i])) == 1 or (float(column2[i])) == 1): 
             a = a + [int(i)+2]
             pass
    return(a)

def endsmile(column1, column2): 
    a = []
    for i in range (1, len(column1)):
        if (float(column1[i]) == 0 and (float(column2[i])  == 0)):
            #return(i)
            if((float(column1[i-1])) == 1 or (float(column2[i-1])) == 1):
                 a = a + [int(i)+2]
                 pass

    return(a)


def write_videofile(clip_start, clip_end, num):
        try:
            clip = VideoFileClip('PA02.mp4').subclip(clip_start, clip_end) ################################name of the video here###############
            print(clip_start, clip_end)
            clip.write_videofile("output_%s.mp4" % num, bitrate="4000k",
                                threads=1, preset='ultrafast', codec='h264')
        except:
            print("error", clip_start, clip_end)

if __name__ == "__main__":
    print("I am readin the file, lads ")
    smilestarts, smileends, look1, look2 = makeData()
    print("Number of smiles: ", len(smilestarts), ", ", len(smileends))
    #''' delete this hash to comment out the eyegaze stuff%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    print("Starting to look for eye gazes!")
    a, b, c, d, which_corner_is_it = gazecalibration(smilestarts[1])
    look1, look2 = eyeGazeLocations()
    #find_all_smiles(look1, look2, a, b, c, d, which_corner_is_it)
    gaze_by_condition(find_all_smiles(look1, look2, a, b, c, d, which_corner_is_it) , smilestarts[0])
    #''' delete this hash to comment out the eyegaze stuff%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ''' delete this hash to comment out the video stuff%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    original_video = VideoFileClip('PA02.mp4') #############################name of the video here#########################
    print("I started")
    duration = original_video.duration
    clip_start = 0 
    i = 0
    num = 0
    while clip_start < duration:
        if i == len(smilestarts):
            clip_end = duration
            print("I have reached the end of the array!")
            break 
        clip_start = (smilestarts[i] *10/100) #####add the number of centiseconds each row is
        print("Current start:", i)
        clip_end = (smileends[i] * 10/100) #####add the number of centiseconds each row is
        print("Current end:", i)
        print("duration of the video:", (clip_end - clip_start))     
        if clip_end > duration:
                clip_end = duration
                print("I have reached the end of the video!")
        if (clip_end - clip_start) < 3.00:
            clip_end = (smileends[i+1] * 10/100)
        else: 
            p = Process(target=write_videofile, args=(clip_start, clip_end, num)).start()
        i += 1
        print("Adding to i: ", i)
        num += 1
        print("Adding to num: ", num)
        ''' #delete this hash to comment out the video stuff%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

