import hashlib,sqlite3

f="rainDB.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

q = "CREATE TABLE users (user TEXT, pass TEXT)"
c.execute(q)

'''
q = "INSERT INTO users VALUES(\'admin\', \'%s\')" %(hashlib.sha1("pass").hexdigest())
c.execute(q)
'''


db.commit() #save changes
db.close()  #close database
