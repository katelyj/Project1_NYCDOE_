import spotipy, urllib2, os
from playsound import playsound


spotify = spotipy.Spotify()

#get song in mp3 format
searchRet = spotify.search("genre:blues", limit=1, offset=0, type='track')
songUrl = searchRet['tracks']['items'][0]['preview_url']

#download
f = urllib2.urlopen(songUrl)
data = f.read()
with open("song.mp3", "wb") as code:
    code.write(data)


#play
playsound('song.mp3')
#cleanup
os.remove("song.mp3")
