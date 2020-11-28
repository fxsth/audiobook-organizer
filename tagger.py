import os
from metadata import Audiobookmeta
from PIL import Image
import requests
import eyed3

def tagAllInDirectory(dir, audiobookmeta):
    for file in os.listdir(dir):
        print(audiobookmeta.searchterm)
        audiofile = eyed3.load(dir+"/"+file)
        audiofile.tag.artist = audiobookmeta.artistName
        audiofile.tag.album = audiobookmeta.collectionName
        audiofile.tag.album_artist = audiobookmeta.artistName
        audiofile.tag.title = file.split('.')[0]
        # audiofile.tag.genre = audiobookmeta.primaryGenreName
        # audiofile.tag.comment = audiobookmeta.description
        # Cover:
        response = requests.get(audiobookmeta.artworkUrl)
        imagedata = response.content
        audiofile.tag.images.set(3,imagedata,"image/jpeg",u"album cover")
        audiofile.tag.save()

