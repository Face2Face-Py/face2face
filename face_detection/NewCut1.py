import glob
from shutil import copyfile

##emotions = ["neutral", "anger", "disgust", "happy", "surprise"]
emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotion order
participants = glob.glob("source_emotion/*") #Returns a list of all folders with participant numbers
#print (participants)
pessoa = glob.glob("source_emotion/*")

for x in participants:
    part = "%s" %x[-4:] #store current participant number
    for sessions in glob.glob("%s/*" %x): #Store list of sessions for current participant
        for files in glob.glob("%s/*txt" %sessions):
            current_session = files[20:-30]
            file = open(files, 'r')
            print(files, file)

            emotion = int(float(file.readline())) #emotions are encoded as a float, readline as float, then convert to integer.

            print("emotion: ", emotion)

            #sorted(fi, key = lambda name: int (name[9:-4]))
            #print (file)
            if  not (emotion == 2 or emotion == 3 or emotion == 4):
                sourcefile_emotion = sorted(glob.glob("source_images/%s/%s/*.png" %(part, current_session)))[-1] #get path for last image in sequence, which contains the emotion
                sourcefile_neutral = sorted(glob.glob("source_images/%s/%s/*.png" %(part, current_session)))[0] #do same for neutral image
        
                print(sourcefile_emotion)
                print(sourcefile_neutral)

                dest_neut = "sorted_set/neutral/%s" %sourcefile_neutral[25:] #Generate path to put neutral image
                dest_emot = "sorted_set/%s/%s" %(emotions[emotion], sourcefile_emotion[25:]) #Do same for emotion containing image
                
                copyfile(sourcefile_neutral, dest_neut) #Copy file
                copyfile(sourcefile_emotion, dest_emot) #Copy file