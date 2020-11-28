import os
from metadata import Audiobookmeta
from mp3_tagger import MP3File, VERSION_2

def tagAllInDirectory(dir, audiobookmeta):
    for file in os.listdir(dir):
        print(audiobookmeta.searchterm)
        mp3file = MP3File(dir+"/"+file)
        mp3file.set_version(VERSION_2)
        mp3file.song = file.split('.')[0]
        mp3file.album = audiobookmeta.collectionName
        mp3file.artist = audiobookmeta.artistName
        mp3file.genre = audiobookmeta.primaryGenreName
        mp3file.comment = audiobookmeta.description
        # print(tags)
        mp3file.save()
