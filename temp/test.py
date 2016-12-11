import subprocess, spotipy, urllib2, os

spotify = spotipy.Spotify()

#get song in mp3 format
searchRet = spotify.search("genre:blues", limit=1, offset=0, type='track')
songUrl = searchRet['tracks']['items'][0]['preview_url']

#download
f = urllib2.urlopen(songUrl)
data = f.read()
with open("song.mp3", "wb") as code:
    code.write(data)

#change to wav
subprocess.call(['ffmpeg', '-i', 'song.mp3', 'song.wav'])

audio_file = "song.wav"

#play
return_code = subprocess.call(["afplay", audio_file])

#cleanup
os.remove("song.wav")
os.remove("song.mp3")
