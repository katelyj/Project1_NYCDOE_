from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3
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
    return render_template("savedSongs.html", userStatus=loggedIn())


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
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/accountsettings/", methods = ["POST", "GET"])
def accountsettings():
    if "user" not in session:
        return redirect(url_for("home"))
    
    if request.method =="GET":
        return render_template("accountSettings.html", userStatus=loggedIn())

    else: pass_message = changePass(session["user"],request.form["oldpass"],request.form["newpass"])
    return render_template("accountSettings.html", status = pass_message, userStatus=loggedIn())
    

@app.route("/search/", methods=["GET", "POST"])
def search_cities():
    # for input of a city, returns a psuedo search page
    # ARGUMENT IS A DICT
    #  f = city_list.db or whatever
    #  db = sqlite3.connect(f)
    #  c = db.cursor()
    #  d = {}
    #  q = "SELECT city, cityid from cities"
    #  l = c.execute(q)
    #  for place in l:
    #     if request.args["city"] in place[0]:
    #         d[place[0]] = place[1]
    # return d // would allow you to take dict and format it so user can pick
    return render_template("search.html")


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
