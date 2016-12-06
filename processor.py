import sqlite3

special = ['snowing','raining','cloudy']

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

def main(condition, temp):

    if condition not in special:
        condition = tempCondition(temp)

    #db stuff
    f="weather.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    query = "SELECT genre FROM weather WHERE mode='%s'"%(condition)
    genre = c.execute(query).fetchall()
    genre = genre[0][0]

    db.close()  #close database
    print genre
    return genre

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
