import sqlite3, urllib2, spotipy, random, json, os, pyglet, time, requests


special = ['snowing','raining','cloudy']
genreList = ["christmas","alternative pop/rock", "blues", "classical", "rock", "rap", "folk", "latin"]
player = pyglet.media.Player()


#returns the temperature condition given the current temperature
#if there is an issue w/temp, just return "nice" by default
def tempCondition(temp):
    if not isinstance(temp,int):
        return "nice"
    if temp < 0:
        return "freezing"
    if temp < 40:
        return "cold"
    if temp < 60:
        return "nice"
    if temp < 80:
        return "warm"
    return "hot"


def getTracks(givenGenre, number):

    #if there is an error, you have to listen to blues
    #b/c you make me sad
    if givenGenre not in genreList:
        givenGenre = "blues"

    spotify = spotipy.Spotify()
    trackList = []

    while len(trackList) < number:
        #NOTE: using 1000 arbitrarily; will find way to get # songs of certain
        #genres from spotify
        n = random.randrange(1000)
        searchRet = spotify.search("genre:" + givenGenre, limit=1, offset=n, type='track')
        song = searchRet['tracks']['items'][0]['preview_url']
        trackList.append(song)

    return trackList


def download(track, title):
    f = urllib2.urlopen(track)
    data = f.read()
    with open(title, "wb") as code:
        code.write(data)

def play(trackList, user):

    player.volume=1.0

    n = 0
    for track in trackList:
        title = user + str(n) + ".mp3"
        download(track, title)
        song = pyglet.media.load(title)
        player.queue(song)

    player.play()

    for i in range(len(trackList) - 1):
        #pause for 30 seconds
        time.sleep(30)
        #next song
        player.next_source()

    try:
        pyglet.app.run()
    except KeyboardInterrupt:
        pass



def main(condition, temp, username):
    if condition in genreList:
        genre = condition
    else:
        if condition not in special:
            condition = tempCondition(temp)

        #db stuff
        f="database.db"
        db = sqlite3.connect(f) #open if f exists, otherwise create
        c = db.cursor()    #facilitate db ops

        query = "SELECT genre FROM weather WHERE mode='%s'"%(condition)
        genre = c.execute(query).fetchall()
        genre = genre[0][0]

        db.close()  #close database

    trackList = getTracks(genre, 5)
    title = play(trackList, username)

def pause():
    player.pause()




def get_saved_songs(username):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    song_count = 0
    song_str = ""
    query = "SELECT * FROM SavedSongs where user = \'%s\'"%(username)
    dbSavedSongs = c.execute(query)
    for entry in dbSavedSongs:
        song_str+= "<p>%s. Song ID: %d\n City ID: %d\n</p>"%(song_count, entry[0],entry[2])
        song_count+=1
    if (song_count == 0): song_str+= "You currently have no songs saved."
    return song_str

def get_loc_coords():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat,lon



'''
#debugging
print "expects holiday"
main("snowing",0)
main("snowing",100)
print "expects rap"
main("",50)
print "expects alt"
main("cloudy",100)
print "expects rap"
main("","")
'''

#main('snowing',25,'Vanna')
