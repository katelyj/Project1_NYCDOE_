from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3, json, requests
from utils import processor


f = "database.db"


app = Flask(__name__)
app.secret_key = '<j\x9ch\x80+\x0b\xd2\xb6\n\xf7\x9dj\xb8\x0fmrO\xce\xcd\x19\xd49\xe5S\x1f^\x8d\xb8"\x89Z'


def register(username, password):
    if (username=="" or password==""): return "Please fill in the username and password fields"

    db = sqlite3.connect(f)
    c = db.cursor()
    query = "SELECT user FROM users"
    dbUsers = c.execute(query)

    for entry in dbUsers:
        if (entry[0] == username):
            return "You are already registered."  #check if username is taken

    hashedPass = hashlib.sha1(password).hexdigest()
    insertQuery = "INSERT INTO users VALUES(\'%s\',\'%s\')"%(username,hashedPass)

    c = db.cursor()
    c.execute(insertQuery)

    db.commit()
    db.close()
    return "You are now successfully registered."


def checkLogin(username,password):
    hashedPass = hashlib.sha1(password).hexdigest()
    db = sqlite3.connect(f)
    c = db.cursor()
    query = "SELECT * FROM users"
    dbUserPass = c.execute(query)
    for entry in dbUserPass:
        if (entry[0] == username):
            if (entry[1] == hashedPass): return ""
            else: return "Incorrect Password"
    return "Incorrect Username"


def changePass(username,oldpass,newpass):
    if (oldpass=="" or newpass==""): return "Please fill in both password fields"
    hashedOldPass = hashlib.sha1(oldpass).hexdigest()
    hashedNewPass = hashlib.sha1(newpass).hexdigest()
    db = sqlite3.connect(f)
    c = db.cursor()
    d = db.cursor()
    query = "SELECT * FROM users"
    dbUserPass = c.execute(query)
    for entry in dbUserPass:
        if (entry[0] == username):
            if (entry[1] == hashedOldPass):

                updateQuery = "UPDATE users SET pass = \'%s\' WHERE user = \'%s\'"%(hashedNewPass,username)
                d.execute(updateQuery)
                db.commit()
                db.close()
                return "You have successfully changed your password"
            else: return "You entered an incorrect password"


def loggedIn():
    if "user" in session:
        return "Logout"
    return "Login"


@app.route("/")
@app.route("/main/")
def main():
    return render_template("main.html")


@app.route("/home/")
def home():
    return render_template("streamingPage.html", userStatus=loggedIn())


@app.route("/saved/")
def save():
    if "user" not in session:
        return redirect(url_for("error"))
    db = sqlite3.connect(f)
    c = db.cursor()
    song_str = ""
    query = "SELECT * FROM SavedSongs where user = \'%s\'"%(session["user"])
    dbSavedSongs = c.execute(query)
    for entry in dbSavedSongs:
        song_str+= "<p>Song ID: %d\n City ID: %d\n</p>"%(entry[0],entry[2])
    if (len(song_str) == 0): song_str = "You currently have no songs saved."
    return render_template("savedSongs.html", userStatus=loggedIn(), song_html=song_str)


@app.route("/login/", methods = ["GET","POST"])
def login():
    if "user" in session:
        return logout()
    
    if request.method == "GET":
        return render_template("login.html", status = "", userStatus=loggedIn())
    
    if request.form["enter"] == "Register":
        register_message = register(request.form["user"],request.form["pass"])
        return render_template("login.html", status = register_message, userStatus=loggedIn())
    
    if request.form["enter"] == "Login":
        login_message = checkLogin(request.form["user"],request.form["pass"])
        if (login_message == ""):
            session["user"] = request.form["user"]
            return redirect(url_for("home"))
        
        return render_template("login.html", status = login_message, userStatus=loggedIn())


@app.route("/error/", methods = ["POST", "GET"])
def error():
    return render_template("error.html", userStatus=loggedIn())


@app.route("/logout/")
def logout():
    session.pop("user")
    return redirect(url_for("home"))


@app.route("/accountsettings/", methods = ["POST", "GET"])
def accountsettings():
    if "user" not in session:
        return redirect(url_for("error"))
    
    if request.method =="GET":
        return render_template("accountSettings.html", userStatus=loggedIn())

    else: pass_message = changePass(session["user"],request.form["oldpass"],request.form["newpass"])
    return render_template("accountSettings.html", status = pass_message, userStatus=loggedIn())


@app.route("/update/", methods = ["POST", "GET"])
def updateLocation():
    return redirect(url_for("main"))
    

@app.route("/search/", methods=["GET", "POST"])
def search_cities():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    loc_msg = "We found your location: (%s , %s)"%(lat,lon)
    #LAT AND LON info here to be used for weather
    return render_template("search.html", status = loc_msg)


@app.route("/find_me/")
def find_me():
    # grab location
    return render_template("streamingPage.html", userStatus=loggedIn()) #argument of song?


@app.route("/choose/")
def choose():
    return render_template("main.html") # argument of song?
    # could clean up later once main() function gets cleared up

    
#NOTE: can give arg to song, let user choose genre
@app.route("/stream/")
def song():
    url = processor.main('snowing',45)
    return render_template('streamingPage.html', url = url, userStatus=loggedIn())


if __name__ == "__main__":
    app.debug = True
    app.run()
