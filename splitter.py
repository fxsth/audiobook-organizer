import os
import ffmpeg

def create_dir(path):
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
        stream = (
            ffmpeg
            .input(pathTofile)
            .output(
                outputDir+"/"+titlePrefix+"-%03d.mp3", 
                f='segment', 
                segment_time='1800', 
                acodec='copy'
                # **{ 'metadata':'title='+collectionName, 'metadata:':'artist='+artistName, 'metadata:g':'album='+collectionName,}
                )
        )
        ffmpeg.run(stream,capture_stderr=True, capture_stdout=True)
    except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e

def renameAllAfterSplitting(dir, titlePrefix):
    fileCounter = 0
    totalNumber = len([name for name in os.listdir(dir) if os.path.isfile(dir+"/"+name)])
    titlePrefix = titlePrefix + "-"
    sortedDir = sorted(os.listdir(dir))
    for file in sortedDir:
        if os.path.isfile(dir+"/"+file):   
            fileCounter = fileCounter+1
            outputFileName = titlePrefix
            if(totalNumber>9 and fileCounter<10):
                # 01,02,...,10
                outputFileName = outputFileName + "0"
            if(totalNumber>99 and fileCounter<100):
                # 001,002,...,010,...,100
                outputFileName = outputFileName + "0"
            outputFileName = outputFileName + str(fileCounter) + ".mp3"
            os.rename(dir+"/"+file, dir+"/"+outputFileName)
        