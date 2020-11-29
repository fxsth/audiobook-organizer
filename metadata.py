import requests

api_url = 'https://itunes.apple.com/search?media=audiobook&term='

class Audiobookmeta:
    """Retrieves metadata from Source"""
    searchterm = ""
    collectionName = ""
    artistName = ""
    artworkUrl = ""
    releaseDate = ""
    primaryGenreName = ""
    description = ""
    
    def __init__(self, search):
        self.searchterm = search

    def tryRetrieveFromITunes(self):
        self.searchterm.replace('-', '')
        self.searchterm.replace(':', '')
        self.searchterm.replace('  ', ' ')
        self.searchterm.replace(' ', '%20')
        if(len(self.searchterm)==0):
            print ("Searchterm is empty")
            return False
        try:
            response = requests.get(api_url+self.searchterm).json()
            # print(api_url+self.searchterm)
            if(len(response["results"])<1):
                print ("No audiobook found")
                return False
            result = response["results"][0]
            # print(result)
            self.collectionName = result["collectionName"]
            self.artistName = result["artistName"]
            self.artworkUrl = result["artworkUrl100"]
            self.releaseDate = result["releaseDate"]
            self.primaryGenreName = result["primaryGenreName"]
            self.description = result["description"]
            self.artworkUrl = self.artworkUrl.replace('100x100bb.jpg', '600x600bb.jpg')
            return True
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print ("An error occured while retrieving metadata")
            return False
