import os
import re
import sys
from shutil import copyfile
import ffmpeg
from natsort import natsorted


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

def splitIfNecessary(dir, outputDir, titlePrefix, recursive = False):
    if(os.path.isfile(dir)):
        splitFile(dir, outputDir, titlePrefix)
        return
    fileCounter = 0
    totalNumber = len([name for name in os.listdir(dir) if os.path.isfile(dir+"/"+name)])
    titlePrefix = titlePrefix + "-"
    if(recursive):
        totalNumber = sum([len(files) for r, d, files in os.walk(dir)])
        splitIfNecessaryRecursive(dir, outputDir, titlePrefix, totalNumber)
        return
    filelist = natsorted(os.listdir(dir))
    for element in filelist:
        if os.path.isfile(dir+"/"+element):
            zeros = ""
            fileCounter = fileCounter+1
            if(totalNumber>9 and fileCounter<10):
                # add a zero if more than one digit
                zeros = zeros + "0"
            if (totalNumber > 99 and fileCounter < 100):
                zeros = zeros + "0"
            if (os.path.getsize(dir + "/" + element) < 100000000 and element.endswith('.mp3')):
                copyfile(dir + "/" + element, outputDir + "/" + titlePrefix + zeros + str(fileCounter) + ".mp3")
                print("Copy to: " + outputDir + "/" + titlePrefix + zeros + str(fileCounter) + ".mp3")
            else:
                splitFile(dir+"/"+element, outputDir, titlePrefix + str(fileCounter))

def splitIfNecessaryRecursive(dir, outputDir, titlePrefix, totalNumber ,fileCounter = 0):
    filelist = natsorted(os.listdir(dir))
    for element in filelist:
        if os.path.isfile(dir+"/"+element):
            zeros = ""
            fileCounter = fileCounter+1
            if(totalNumber>9 and fileCounter<10):
                # add a zero if more than one digit
                zeros = zeros + "0"
            if (totalNumber > 99 and fileCounter < 100):
                zeros = zeros + "0"
            if (totalNumber > 999 and fileCounter < 1000):
                zeros = zeros + "0"
            if(os.path.getsize(dir + "/" + element)<100000000 and element.endswith('.mp3')):
                copyfile(dir + "/" + element, outputDir + "/" + titlePrefix + zeros + str(fileCounter) + ".mp3")
                print("Copy to: " + outputDir + "/" + titlePrefix + zeros + str(fileCounter) + ".mp3")
            else:
                splitFile(dir+"/"+element, outputDir, titlePrefix + zeros+ str(fileCounter))
        else:
            fileCounter = splitIfNecessaryRecursive(dir+"/"+element, outputDir, titlePrefix, totalNumber, fileCounter)
    return fileCounter


def splitFile(pathTofile, outputDir, titlePrefix):
    print(pathTofile)
    try:
        if(pathTofile.endswith('.mp3')):
            print("Processing File by copy codec")
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
        elif(pathTofile.endswith('.ini')):
            print("ignoring .ini file")
            return
        else:
            print("Processing File by transcode to mp3")
            stream = (
                ffmpeg
                    .input(pathTofile)
                    .output(
                    outputDir + "/" + titlePrefix + "-%03d.mp3",
                    f='segment',
                    segment_time='7200',
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
    test = os.listdir(dir)
    sortedDir = natsorted(os.listdir(dir))
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
            print("Renaming " + file + " -> " + outputFileName)
            os.rename(dir+"/"+file, dir+"/"+outputFileName)

def getAllFilesInSubdirectoriesAndRename(parentdir, title):
    sortedParentDir = natsorted(os.listdir(parentdir))
    fileCounter = 0
    totalNumber = 0
    for subdir in sortedParentDir:
        totalNumber = totalNumber + len([name for name in os.listdir(parentdir+"/"+subdir) if os.path.isfile(subdir + "/" + name)])
    for subdir in sortedParentDir:
        trackNumber = ""
        sortedDir = natsorted(os.listdir(parentdir+"/"+subdir))
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
                print("Renaming " + file + " -> " + outputFileName)
                os.rename(subdir + "/" + file, parentdir + "/" + outputFileName)

# dir= r"C:\Users\Felix\Downloads\2014-Das_Licht_der_Welt_Die_Fleury-ddlme-zz147329\Daniel Wolf - Das Licht der Welt\Daniel Wolf\Das Licht der Welt"
# prefix = "Das Licht der Welt"
# getAllFilesInSubdirectoriesAndRename(dir, prefix)