import sqlite3

f="SavedSongs.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

q = "CREATE TABLE SavedSongs (songid INT, user TEXT, cityid INT)"
c.execute(q)

#q = "INSERT INTO SavedSongs VALUES(%d,'%s',%d)"%(0,michael,123)
#c.execute(q)

db.commit() #save changes
db.close()  #close database
