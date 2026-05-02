import secrets
from datetime import date
from functools import wraps

from flask import Flask, session, request, render_template, redirect, abort, flash

import config
import data


def check_csrf(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.form["csrf_token"] != session["csrf_token"]:
            abort(400)
        else:
            return f(*args, **kwargs)
    return wrapper

def require_login(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Toiminto vaatii kirjautumisen")
            return redirect("/login")
        else:
            return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
app.config.from_pyfile("config.py")


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
    if len(name) > 20:
        abort(400)
    passwd1 = request.form["password1"]
    passwd2 = request.form["password2"]
    if passwd1 != passwd2:
        flash("Salasanat eivät täsmää", "error")
        return redirect("/register")
    user_id = data.create_user(name, passwd1)
    if user_id is None:
        flash("Käyttäjänimi on jo varattu", "error")
        return redirect("/register")
    flash("Käyttäjän luonti onnistui. Ole hyvä, ja kirjaudu sisään.")
    return redirect(f"/login")


@app.route("/login")
def login():
    if "user_id" in session:
        flash(f"Olet jo kirjautunut sisään käyttäjällä {session['username']}.")
        return redirect("/")
    return render_template("login.html")


@app.route("/do-login", methods=["POST"])
def do_login():
    name = request.form["username"]
    passwd = request.form["password"]
    user_id = data.check_login(name, passwd)
    if not user_id:
        flash("Virheellinen käyttäjätunnus tai salasana", "error")
        return redirect("/login")
    session["user_id"] = user_id
    session["username"] = name
    session["csrf_token"] = secrets.token_hex(16)
    flash("Sisäänkirjautuminen onnistui.")
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    flash("Uloskirjautuminen onnistui.")
    return redirect("/")


@app.route("/users/<int:user_id>")
def user_page(user_id):
    user = data.get_user(user_id)
    if not user:
        abort(404)
    
    post_count = data.get_user_post_count(user_id)
    reservation_count = data.get_user_reservation_count(user_id)
    posts = data.get_user_posts(user_id)
    return render_template("user.html", user=user, post_count=post_count, reservation_count=reservation_count, posts=posts)


@app.route("/posts")
def posts():
    query = request.args.get("query", "")
    posts = data.search_posts(query)
    count = len(posts)
    return render_template("posts.html", query=query, count=count, posts=posts)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    post = data.get_post(post_id)
    if not post:
        abort(404)
    
    if "user_id" in session:
        data.add_post_view(session["user_id"], post_id)
    count = data.get_post_viewer_count(post_id)

    today_str = date.today().isoformat()
    reservations = data.get_post_reservations(post_id, today_str)
    return render_template("post.html", post=post, view_count=count, today=today_str, reservations=reservations)


@app.route("/new-post")
@require_login
def new_post():
    return render_template("editor.html", mode="new")


@app.route("/do-new-post", methods=["POST"])
@require_login
@check_csrf
def add_post():
    item = request.form["item"][:50]
    info = request.form["info"][:1000]
    post_id = data.create_post(session["user_id"], item, info)
    flash("Ilmoitus luotu.")
    return redirect(f"/posts/{post_id}")


@app.route("/edit-post/<int:post_id>")
@require_login
def edit_post_page(post_id):
    post = data.get_post(post_id)
    if not post:
        abort(404)
    return render_template("editor.html", mode="edit", post=post, item_value=post["item"], info_value=post["info"])


@app.route("/do-edit-post/<int:post_id>", methods=["POST"])
@require_login
@check_csrf
def edit_post(post_id):
    post = data.get_post(post_id)
    if not post:
        abort(404)
    if post["author"] != session["user_id"]:
        abort(403)
    
    item = request.form["item"][:50]
    info = request.form["info"][:1000]
    data.edit_post(post_id, item, info)
    flash("Muokkaus onnistui.")
    return redirect(f"/posts/{post_id}")


@app.route("/remove-post/<int:post_id>")
@require_login
def remove_post_page(post_id):
    post = data.get_post(post_id)
    if not post:
        abort(404)
    return render_template("remove-post.html", post=post)


@app.route("/do-remove-post/<int:post_id>", methods=["POST"])
@require_login
@check_csrf
def remove_post(post_id):
    post = data.get_post(post_id)
    if not post:
        abort(404)
    if post["author"] != session["user_id"]:
        abort(403)
    if "continue" in request.form:
        data.remove_post(post_id)
        flash("Ilmoitus poistettu.")
        return redirect("/posts")
    else:
        return redirect(f"/posts/{post_id}")
    

@app.route("/do-add-reservation/<int:post_id>", methods=["POST"])
@require_login
def add_reservation(post_id):
    start_date_str = request.form["start_date"]
    end_date_str = request.form["end_date"]

    start_date = date.fromisoformat(start_date_str)
    end_date = date.fromisoformat(end_date_str)

    if start_date > end_date:
        flash("Varauksen alkupäivä ei voi olla päättymispäivän jälkeen.")
        return redirect(f"/posts/{post_id}")

    reservations = data.get_post_reservations(post_id, start_date_str, end_date_str)
    if len(reservations) > 0:
        flash("Tälle ajalle on jo varaus.", "error")
        return redirect(f"/posts/{post_id}")

    reservation = data.add_reservation(post_id, session["user_id"], start_date_str, end_date_str)
    flash("Varaus luotu onnistuneesti.")
    return redirect(f"/posts/{post_id}")


@app.route("/remove-reservation/<int:reservation_id>")
@require_login
def remove_reservation_page(reservation_id):
    reservation = data.get_reservation(reservation_id)
    if not reservation:
        abort(404)
    return render_template("remove-reservation.html", reservation=reservation)


@app.route("/do-remove-reservation/<int:reservation_id>", methods=["POST"])
@require_login
@check_csrf
def remove_reservation(reservation_id):
    reservation = data.get_reservation(reservation_id)
    if not reservation:
        abort(404)
    if reservation["user_id"] != session["user_id"]:
        abort(403)
    if "continue" in request.form:
        data.remove_reservation(reservation_id)
    
    flash("Varaus poistettu.")
    return redirect(f"/posts/{reservation["post"]}")