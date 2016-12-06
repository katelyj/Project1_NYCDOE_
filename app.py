from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3
#from utils import 

f="rainDB.db"

app = Flask(__name__)
app.secret_key = '<j\x9ch\x80+\x0b\xd2\xb6\n\xf7\x9dj\xb8\x0fmrO\xce\xcd\x19\xd49\xe5S\x1f^\x8d\xb8"\x89Z'

def register(username, password):
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

@app.route("/")
@app.route("/homepage/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("homepageTemplate.html")

@app.route("/login/", methods = ["GET","POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("loginTemplate.html", status = "")
    if request.form["enter"] == "Register":
        register_message = register(request.form["user"],request.form["pass"])
        return render_template("loginTemplate.html", status = register_message)
    if request.form["enter"] == "Login":
        login_message = checkLogin(request.form["user"],request.form["pass"])
        if (login_message == ""):
            session["user"] = request.form["user"]
            return redirect(url_for("home"))
        return render_template("loginTemplate.html", status = login_message)

@app.route("/logout/")
def logout():
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/search/", methods=["GET"])
def search():
    #check which button they picked
    #if request.args["find_me"]
    #   use maps api to locate person// maybe database?
    #elif request.args["enter_city"]
    #  f = city_list.db or whatever
    #  db = sqlite3.connect(f)
    #  c = db.cursor()
    #  q = "SELECT city from cities"
    #  c.execute(q)
    return render_template("search.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
