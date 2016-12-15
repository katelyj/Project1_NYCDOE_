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


def checkZip(zipcode):
    if (len(str(zipcode)) != 5): return False
    else: return True


@app.route("/")
@app.route("/main/")
def main():
    return render_template("main.html")


@app.route("/home/", methods = ["GET","POST"])
def home():
    return render_template("streamingPage.html", userStatus=loggedIn())


@app.route("/saved/", methods = ["GET","POST"])
def save():
    if "user" not in session:
        return redirect(url_for("login"))
    if "save_song" in request.form:
        print "starting"
        song_url = request.form['url']
        print song_url
        artist = request.form['artist']
        print artist
        title = request.form['title']
        print title
        print song_url + "  " + title + "  " + artist
        saved_msg = addSavedSong(song_url,session["user"],title,artist)
        print "saved"
    song_str = processor.get_saved_songs(session["user"])
    return render_template("savedSongs.html", userStatus=loggedIn(), song_html=song_str)


def addSavedSong(url,user,title,artist):
    db = sqlite3.connect(f)
    c = db.cursor()
    query = "INSERT INTO SavedSongs VALUES(\'%s\',\'%s\', \'%s\',\'%s\')"%(url,user,title,artist)
    c.execute(query)

    db.commit()
    db.close()

    return "Your song has been saved"


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

    
@app.route("/logout/")
def logout():
    if "user" in session: session.pop("user")
    if "coords" in session: session.pop("coords")
    return redirect(url_for("home"))


@app.route("/accountsettings/", methods = ["POST", "GET"])
def accountsettings():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method =="GET":
        return render_template("accountSettings.html", userStatus=loggedIn())

    else: pass_message = changePass(session["user"],request.form["oldpass"],request.form["newpass"])
    return render_template("accountSettings.html", status = pass_message, userStatus=loggedIn())


@app.route("/update/", methods = ["POST", "GET"])
def updateLocation():
    return redirect(url_for("main"))


@app.route("/search/", methods=["GET", "POST"])
def search():

    #clear
    if 'zipcode' in session:
        session.pop('zipcode')
    if 'coords' in session:
        session.pop('coords')

    #zipcode
    if "zipcode" in request.form:
        zipcode = request.form["zipcode"]
        #print(request.form["zipcode"])
        #print checkZip(zipcode)
        if(checkZip(zipcode)):
            session["zipcode"] = zipcode
            return song()
        else:
            return redirect(url_for("main"))#, status = "Please enter a valid zipcode")

    #coords
    else:
        lat,lon = processor.get_loc_coords()
        loc_msg = "We found your location: (%s , %s)"%(lat,lon)
        session["coords"] = [lat,lon]
        return render_template("search.html", status = loc_msg)

    
#NOTE: can give arg to song, let user choose genre


def getWeather():
    send_url = "http://api.openweathermap.org/data/2.5/forecast/"

    if "zipcode" in session:
        send_url += "weather?zip="
        z = session["zipcode"]
        send_url += z
        send_url += ",us"

    elif "coords" in session:
        send_url += "weather?lat="
        [c,o] = session["coords"]
        send_url += str(c)
        send_url += "&lon="
        send_url += str(o)

    else:
        return redirect(url_for("main")) #lol

    send_url += "&units=imperial"
    send_url += "&APPID=b2b943fba8b13d5ee10731cdade75c9a"#add KEY
    # remember to deal with above
    r = requests.get(send_url)
    j = json.loads(r.text)
    cond = j['list'][0]['weather'][0]['main']
    temp = j['list'][0]['main']['temp']
    return(cond, temp)


@app.route("/stream/")
def song():
    args = getWeather()
    cond = args[0]
    temp = args[1]
    song = processor.main(cond,temp)
    return render_template('streamingPage.html', url = song['url'], title = song['title'], artist = song['artist'], genre = song['genre'], userStatus=loggedIn())


if __name__ == "__main__":
    app.debug = True
    app.run()
