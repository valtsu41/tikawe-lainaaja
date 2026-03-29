from datetime import datetime

from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)

@app.route("/")
def index():
    db.execute("INSERT INTO Visits (visited_at) VALUES (datetime('now'))")
    visit_count = db.query("SELECT COUNT(*) AS c FROM Visits")[0]["c"]
    return render_template("index.html", visit_count=visit_count)

@app.route("/new")
def new_post():
    return render_template("new.html")

@app.route("/posts")
def posts():
    posts = db.query("SELECT * FROM Posts")
    count = len(posts)
    return render_template("posts.html", count=count, posts=posts)

@app.route("/posts", methods=("POST",))
def add_post():
    username = request.form["username"]
    item = request.form["item"]
    db.execute("INSERT INTO Posts (author, item) VALUES (?, ?)", (username, item))
    return redirect("/posts")

