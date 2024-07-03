import subprocess, os
from json import dump
from pytube import Search

from datetime import datetime, time, timezone, timedelta
tz=timezone(timedelta(hours=-3))

def parseDate(seconds):
    date=datetime.fromtimestamp(seconds, tz)
    date=date.strftime('%d/%m/%Y %H:%M:%S')
    return date

#Aware of the below when updating.
# Changed in version 3.12: st_ctime is deprecated on Windows.
# Use st_birthtime for the file creation time. In the future, 
# st_ctime will contain the time of the most recent metadata change, 
# as for other platforms.


invalidChars='/:*?"\'<>|\\~.#,'
ob={}

def removeInvalidCharacters(string):
    #Some characters are not included when pytube downloads a video, so they would mess with the Exatch Match
    purifiedString=''
    for char in string:
        if char in invalidChars:
            continue
        purifiedString+=char
    return purifiedString

def customStringCleaning(string):
    #remove .mp3/mp4
    string=string[:-4]
    if ' (320 kbps)' in string:
        index=string.find(' (320 kbps)')
        string=string[:index]+string[index+11:]
    return string

def isVideoOrAudio(string):
    if string[:-1].endswith('.mp'):
        return True
    return False
    

def returnVideoDuration(filename):
    result=subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of",
                            "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    #print(result)
    #print(filename)
    print('\n'+'-'*32)
    # print(result.stdout.decode())
    return float(result.stdout.decode())

def getFolderObject(string, basePath):
    filename=os.path.basename(string)
    string=os.path.dirname(string)
    if string==basePath:
        string=''
    else:
        string=string.removeprefix(basePath+'\\')
    string=string.split('\\')

    currentFolder=ob
    if string!=['']:
        for folder in string:
            if folder not in currentFolder:
                currentFolder[folder]={}
            currentFolder=currentFolder[folder]
    currentFolder[filename]={}
    return currentFolder[filename]

def formatTime(seconds):
    #Will return a string in a time format like this "4:01:23" or this "1:23"
    # print(seconds)
    length=''
    if seconds>=3600:
        length+=f'{seconds//3600}:'
        length+=f'{(seconds%3600//60):0>2}:'
    else:
        length+=f'{seconds//60}:'
    length+=f'{(seconds%60):0>2}'
    print(length)
    return length




def log(pathtotest):

    base=pathtotest
    #Making sure the json file name is unique and doesn't overwrite previous logs, better a redundant collection
    #than losing import information.
    jsonFileName=os.path.basename(base)
    folderNumber=1
    while os.path.isfile(f'{base}\\{jsonFileName}.json'):
        jsonFileName=os.path.basename(base)+' '+str(folderNumber)
        folderNumber+=1
    # print(jsonFileName)
    videos=[]
    os.chdir(pathtotest)

    #Walking recursively through directories starting on the base one and collecting videos and audios
    for a,b,c in os.walk(os.getcwd()):
        print(a)
        print(b)
        print(c)
        print('\n\n')
        for file in c:
            if isVideoOrAudio(file):
                videos.append(a+'\\'+file)

    for videoPath in videos[:]:
        videoObject=getFolderObject(videoPath, base)
        chosenVideo=None
        possibleVideos=[]
        roundedLength=round(float(returnVideoDuration(videoPath)))
        # print(roundedLength)
        videoName=customStringCleaning(os.path.basename(videoPath))
        exactMatchFound=False
        s=Search(videoName)
        ij=0
        print(f'{videoName}\n')
        while exactMatchFound!=True and ij<100:
            for video in s.results[ij:]:
                ij+=1
                if video.length==roundedLength:
                    # print(ij)
                    # print(video.title)
                    # formatTime(video.length)
                    purifiedVideoName=removeInvalidCharacters(video.title)
                    # print(purifiedVideoName)
                    if purifiedVideoName==videoName:
                        exactMatchFound=True
                        chosenVideo=video
                        print('Exact match!')
                        break
                    print('\n')
                    possibleVideos.append(video)
            if exactMatchFound==False:
                s.get_next_results()
        
        if exactMatchFound==False:
            if possibleVideos!=[]:
                chosenVideo=possibleVideos[0]
        if exactMatchFound or possibleVideos!=[]:
            print(f'The chosen video was:\n {chosenVideo.title}')
            videoObject['Youtube']={
                "Title":chosenVideo.title,
                "URL": chosenVideo.watch_url,
                "i":ij
            }
        else:
            print('No match found.')
            videoObject['Youtube']='No match found.'
        print('\n\n')
        filestats=os.stat(videoPath)
        videoObject['Length']=formattedTime=formatTime(roundedLength)
        videoObject['Modification date']=parseDate(filestats.st_mtime)
        videoObject['Creation date']=parseDate(filestats.st_ctime)
        videoObject['Bytes']=filestats.st_size
        videoObject['Megabytes']=round(filestats.st_size/1048576, ndigits=1)
        # print(videoObject)

    #Saving into a json file inside this same folder
    jsonWrapper=[base]
    jsonWrapper.append(ob)

    with open(f'{jsonFileName}.json', 'w', encoding='utf-8') as f:
        dump(jsonWrapper, f, ensure_ascii=False, indent=2)


pathBeingLogged=input('Insert the path to be logged:\n')
while os.path.isdir(pathBeingLogged)!=True:
    pathBeingLogged=input('Path is not a valid directory.\n')

log(pathBeingLogged)


'''
It will be a json
The format will be got by taking the parts of the file path
Folders will be objects containing videos/audios and other folders
A check for the folder will always be done before trying to add anything (function)

And when the "video" object is created, its just add the infos, the simplest part.
'''

# print('\n\n\n')
# print(dd)