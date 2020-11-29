import os
import re
import requests
import eyed3
from metadata import Audiobookmeta

def tagAllInDirectory(dir, audiobookmeta):
    for file in os.listdir(dir):
        numbers = re.findall(r'\d+', file)
        audiofile = eyed3.load(dir+"/"+file)
        audiofile.tag.title = file.split('.')[0]
        audiofile.tag.track = int(numbers[0])
        audiofile.tag.artist = audiobookmeta.artistName
        audiofile.tag.album = audiobookmeta.collectionName
        audiofile.tag.album_artist = audiobookmeta.artistName
        audiofile.tag.genre = audiobookmeta.primaryGenreName
        audiofile.tag.year = int(audiobookmeta.releaseDate[:4])
        # audiofile.tag.comment = audiobookmeta.description didnt work for me?
        # Cover:
        response = requests.get(audiobookmeta.artworkUrl)
        imagedata = response.content
        audiofile.tag.images.set(3,imagedata,"image/jpeg",u"album cover")
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

