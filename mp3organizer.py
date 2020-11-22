import os
import ffmpeg
import requests
import sys
import urllib.request
import ntpath

dir = sys.argv[1]
searchterm = ntpath.basename(dir)
print("Searchterm is: " + searchterm)
if(len(sys.argv)>2):
    searchterm = sys.argv[1]
searchterm.replace('-', '')
searchterm.replace(':', '')
searchterm.replace('  ', ' ')
searchterm.replace(' ', '%20')
api_url = 'https://itunes.apple.com/search?media=audiobook&term='
response = requests.get(api_url+searchterm).json()
print(api_url+searchterm)
result = response["results"][0]
print(result)
collectionName = result["collectionName"]
artistName = result["artistName"]
artworkUrl = result["artworkUrl100"]
# releaseDate = result["releaseDate"]
# primaryGenreName = result["primaryGenreName"]
# description = result["description"]
artworkUrl.replace('100x100bb.jpg', '600x600bb.jpg')
resource = urllib.request.urlretrieve(artworkUrl)
for file in os.listdir(dir):
    filewithoutext = file.split('.')[0]
    print(file)
    try:
        stream = (
            ffmpeg
            .input(dir+file)
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