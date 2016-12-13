import spotipy, urllib2, os
import pyglet


spotify = spotipy.Spotify()

#get song in mp3 format
searchRet = spotify.search("genre:blues", limit=1, offset=0, type='track')
songUrl = searchRet['tracks']['items'][0]['preview_url']

#download
f = urllib2.urlopen(songUrl)
data = f.read()
with open("song.mp3", "wb") as code:
    code.write(data)


#load into pyglet
song = pyglet.media.load("song.mp3")

#make player
player = pyglet.media.Player()
#load song
player.queue(song)

#set volume
player.volume=1.0

#play
player.play()

#run
try:
    pyglet.app.run()
except KeyboardInterrupt:
    pass

#cleanup
os.remove("song.mp3")
