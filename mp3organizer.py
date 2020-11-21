import os
import ffmpeg
import requests
import sys


dir = sys.argv[0]
searchterm = sys.argv[1]
searchterm.replace('-', '')
searchterm.replace('  ', ' ')
searchterm.replace(' ', '%20')
api_url = 'https://itunes.apple.com/search?media=audiobook&term='
response = requests.get(api_url+searchterm).json()
result = response["results"][0]
print(result)
collectionName = result["collectionName"]
artistName = result["artistName"]
# artworkUrl100 = result["artworkUrl100"]
# releaseDate = result["releaseDate"]
# primaryGenreName = result["primaryGenreName"]
# description = result["description"]

# resource = urllib.request.urlretrieve(artworkUrl100)
for file in os.listdir(dir):
    filewithoutext = file.split('.')[0]
    print(file)
    try:
        stream = (
            ffmpeg
            .input(dir+file)
            # .input(resource[0])
            .output(
                filewithoutext+"-%d.mp3", 
                f='segment', 
                segment_time='3600', 
                acodec='copy', 
                **{ 'metadata':'title='+collectionName, 'metadata:':'artist='+artistName, 'metadata:g':'album='+collectionName,}
                )
        )
        ffmpeg.run(stream,capture_stderr=True, capture_stdout=True)
    except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e