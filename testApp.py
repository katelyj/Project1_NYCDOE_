from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3
#from utils import 

app = Flask(__name__)
app.secret_key = '<j\x9ch\x80+\x0b\xd2\xb6\n\xf7\x9dj\xb8\x0fmrO\xce\xcd\x19\xd49\xe5S\x1f^\x8d\xb8"\x89Z'

@app.route("/")
def default():
    return render_template("search.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
