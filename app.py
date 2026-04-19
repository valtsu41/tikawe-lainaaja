from datetime import datetime
import sqlite3

from flask import Flask, session, request, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash

import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    db.execute("INSERT INTO Visits (visited_at) VALUES (datetime('now'))")
    visit_count = db.query("SELECT COUNT(*) AS c FROM Visits")[0]["c"]
    return render_template("index.html", visit_count=visit_count)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/do-register", methods=["POST"])
def do_register():
    name = request.form["username"]
    passwd1 = request.form["password1"]
    passwd2 = request.form["password2"]
    if passwd1 != passwd2:
        return "Salasanat eivät täsmää"
    passwd_hash = generate_password_hash(passwd1)
    try:
        db.execute("INSERT INTO Users (username, password_hash) VALUES (?, ?)", [name, passwd_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/do-login", methods=["POST"])
def do_login():
    name = request.form["username"]
    passwd = request.form["password"]

    passwd_hash = db.query("SELECT password_hash FROM Users WHERE username = ?", [name])[0][0]
    if check_password_hash(passwd_hash, passwd):
        session["username"] = name
        return redirect("/")
    else:
        return "Virheellinen käyttäjätunnus tai salasana"



@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new-post")
def new_post():
    if "username" not in session:
        return redirect("/login")
    return render_template("new-post.html")

@app.route("/posts")
def posts():
    posts = db.query("SELECT * FROM Posts")
    count = len(posts)
    return render_template("posts.html", count=count, posts=posts)

@app.route("/posts", methods=["POST"])
def add_post():
    item = request.form["item"]
    db.execute("INSERT INTO Posts (author, item) VALUES (?, ?)", (session["username"], item))
    return redirect("/posts")

@app.route("/post/<int:post_id>")
def get_post(post_id):
    res = db.query("SELECT author, item FROM Posts WHERE id = ?", [post_id])
    if not res:
        abort(404)
    return render_template("post.html", post=res[0])
    