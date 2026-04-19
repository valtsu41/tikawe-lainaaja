from datetime import datetime
import sqlite3

from flask import Flask, session, request, render_template, redirect, abort

import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    data.add_visit()
    visit_count = data.get_visit_count()
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
    user_id = data.create_user(name, passwd1)
    if user_id is None:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/do-login", methods=["POST"])
def do_login():
    name = request.form["username"]
    passwd = request.form["password"]
    if (user_id := data.check_login(name, passwd)):
            session["user_id"] = user_id
            session["username"] = name
            return redirect("/")
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
    query = request.args.get("query", "")
    posts = data.search_posts(query)
    count = len(posts)
    return render_template("posts.html", query=query, count=count, posts=posts)

@app.route("/do-new-post", methods=["POST"])
def add_post():
    item = request.form["item"]
    info = request.form["info"]
    post_id = data.create_post(session["user_id"], item, info)
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>")
def get_post(post_id):
    if not (post := data.get_post(post_id)):
        abort(404)
    data.add_post_view(session["user_id"], post_id)
    count = data.get_post_viewer_count(post_id)
    return render_template("post.html", post=post, view_count=count)
