import sqlite3, urllib2, spotipy, random


special = ['snowing','raining','cloudy']
genreList = ["christmas","alternative pop/rock", "blues", "classical", "rock", "rap", "folk", "latin"]

#functional part
urlStart = "https://embed.spotify.com/?uri=spotify:trackset:"
#pretty part
urlEnd = "&theme=white&view=coverart"


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
        song = searchRet['tracks']['items'][0]['id']
        trackList.append(song)

    tracks = ""
    for i in trackList:
        tracks += i + ","
    return tracks

def main(condition, temp):

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
    tracks = getTracks(genre, 5)
    url = urlStart + genre + ":" + tracks + urlEnd
    return url


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


def getLat():
    l = urlib2.urlopen("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBWbZpAXvGSbfDOaGmPql0T3NM-0N5PvHY")

def getLat():
    l = urlib2.urlopen("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBWbZpAXvGSbfDOaGmPql0T3NM-0N5PvHY")
