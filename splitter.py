import os
import sys

import ffmpeg

def create_dir(path):
    if(os.path.exists(path)):
        return False
    try:
        os.makedirs(path)
    except OSError as e:
        print ("Creation of the directory %s failed" % path)
        print(e.strerror())
        return False
    else:
        print ("Successfully created the directory %s " % path)
        return True

def splitIfNecessary(dir, outputDir, titlePrefix):
    fileCounter = 0
    totalNumber = len([name for name in os.listdir(dir) if os.path.isfile(dir+"/"+name)])
    titlePrefix = titlePrefix + "-"
    for file in os.listdir(dir):
        if os.path.isfile(dir+"/"+file):   
            fileCounter = fileCounter+1
            if(totalNumber>9 and fileCounter<10):
                # add a zero if more than one digit
                titlePrefix = titlePrefix + "0"
            splitFile(dir+"/"+file, outputDir, titlePrefix + str(fileCounter))


def splitFile(pathTofile, outputDir, titlePrefix):
    print(pathTofile)
    try:
        if(pathTofile.endswith('.mp3')):
            stream = (
                ffmpeg
                .input(pathTofile)
                .output(
                    outputDir+"/"+titlePrefix+"-%03d.mp3",
                    f='segment',
                    segment_time='3600',
                    acodec='copy'
                    )
            )
        else:
            stream = (
                ffmpeg
                    .input(pathTofile)
                    .output(
                    outputDir + "/" + titlePrefix + "-%03d.mp3",
                    f='segment',
                    segment_time='3600',
                    acodec='libmp3lame'
                )
            )
        ffmpeg.run(stream,capture_stderr=True, capture_stdout=True)
    except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e



def renameAllAfterSplitting(dir, title):
    fileCounter = 0
    totalNumber = len([name for name in os.listdir(dir) if os.path.isfile(dir+"/"+name)])
    sortedDir = sorted(os.listdir(dir))
    for file in sortedDir:
        trackNumber = ""
        if os.path.isfile(dir+"/"+file):   
            fileCounter = fileCounter+1
            if(totalNumber>9 and fileCounter<10):
                # 01,02,...,10
                trackNumber = trackNumber + "0"
            if(totalNumber>99 and fileCounter<100):
                # 001,002,...,010,...,100
                trackNumber = trackNumber + "0"
            outputFileName = trackNumber + str(fileCounter) + " - " + title + ".mp3"
            os.rename(dir+"/"+file, dir+"/"+outputFileName)

def getAllFilesInSubdirectoriesAndRename(parentdir, title):
    sortedParentDir = sorted(os.listdir(parentdir))
    fileCounter = 0
    totalNumber = 0
    for subdir in sortedParentDir:
        totalNumber = totalNumber + len([name for name in os.listdir(parentdir+"/"+subdir) if os.path.isfile(subdir + "/" + name)])
    for subdir in sortedParentDir:
        trackNumber = ""
        sortedDir = sorted(os.listdir(parentdir+"/"+subdir))
        for file in sortedDir:
            if os.path.isfile(subdir + "/" + file):
                fileCounter = fileCounter + 1
                if (totalNumber > 9 and fileCounter < 10):
                    # 01,02,...,10
                    trackNumber = trackNumber + "0"
                if (totalNumber > 99 and fileCounter < 100):
                    # 001,002,...,010,...,100
                    trackNumber = trackNumber + "0"
                outputFileName = trackNumber + str(fileCounter) + " - " + title + ".mp3"
                os.rename(subdir + "/" + file, parentdir + "/" + outputFileName)

# dir= r"C:\Users\Felix\Downloads\2014-Das_Licht_der_Welt_Die_Fleury-ddlme-zz147329\Daniel Wolf - Das Licht der Welt\Daniel Wolf\Das Licht der Welt"
# prefix = "Das Licht der Welt"
# getAllFilesInSubdirectoriesAndRename(dir, prefix)