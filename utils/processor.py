import sqlite3, urllib2, spotipy


special = ['snowing','raining','cloudy']
genreList = ["christmas","alternative pop/rock", "blues", "classical", "rock", "rap", "folk", "latin"]

#functional part
urlStart = "https://embed.spotify.com/?uri=spotify:trackset:"
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
    trackList = []
    #while len(trackList < number):
    #    getNewTrack(genre)
    #trackString = ""
    #for i in trackList:
    #    trackString += i + ","
    sample = "5Z7ygHQo02SUrFmcgpwsKW,1x6ACsKV4UdWS2FMuPFUiT,4bi73jCM02fMpkI11Lqmfe"
    spotify = spotipy.Spotify()

    searchRet = spotify.search("genre:"+givenGenre, limit=number, offset=0, type='track')
    trackList = searchRet['tracks']['items']
    tracks = ""
    for i in trackList:
        tracks += i['id'] + ","
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
