import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

import db


# Visitor counter functions

def get_visit_count():
    return db.query("SELECT COUNT(*) FROM Visits")[0][0]


def add_visit():
    db.execute("INSERT INTO Visits (visited_at) VALUES (datetime('now'))")



# User functions

def check_login(username: str, passwd: str):
    res = db.query("SELECT id, password_hash FROM Users WHERE username = ?", [username])
    if res:
        user_id, passwd_hash = res[0]
        if check_password_hash(passwd_hash, passwd):
            return user_id
    return None


def create_user(username: str, passwd: str):
    passwd_hash = generate_password_hash(passwd)
    try:
        return db.execute("INSERT INTO Users (username, password_hash) VALUES (?, ?)", [username, passwd_hash])
    except sqlite3.IntegrityError:
        return None


def get_user(user_id: int):
    res = db.query("SELECT id, username FROM Users WHERE id = ?", [user_id])
    if res:
        return res[0]
    else:
        return None


def get_user_posts(user_id: int):
    res = db.query("SELECT id, item FROM Posts WHERE author = ?", [user_id])
    return res



# Post functions 

def get_post(post_id: int):
    res = db.query("""
        SELECT P.id AS id,   U.id AS author, U.username As author_name, P.item AS item, P.info AS info
        FROM Posts AS P JOIN Users AS U ON P.author = U.id
        WHERE P.id = ?
    """, [post_id])
    if not res:
        return None
    else:
        return res[0]


def search_posts(query: str):
    sql_query = f"%{query}%"
    return db.query("""
        SELECT P.id AS id, U.id AS author, U.username AS author_name, P.item AS item
        FROM Posts AS P JOIN Users AS U ON P.author = U.id
        WHERE P.item LIKE ?
    """, [sql_query])


def create_post(author_id: int, item: str, info: str):
    return db.execute("INSERT INTO Posts (author, item, info) VALUES (?, ?, ?)", [author_id, item, info])


def edit_post(post_id: int, item: str, info: str):
    return db.execute("UPDATE Posts SET item = ?, info = ? WHERE id = ?", [item, info, post_id])


def remove_post(post_id: int):
    db.execute("DELETE FROM Posts WHERE id = ?", [post_id])



# Post viewer functions

def add_post_view(user_id: int, post_id: int):
    return db.execute("INSERT INTO Views (viewed_at, user, post) VALUES (datetime('now'), ?, ?)", [user_id, post_id])


def get_post_viewer_count(post_id: int):
    return db.query("SELECT COUNT(*) FROM (SELECT DISTINCT user, post FROM Views WHERE post = ?)", [post_id])[0][0]



# Reservation functions
def get_reservation(reservation_id: int):
    return db.query("""
        SELECT R.id id, R.post post, R.user user_id, U.username username, R.start_date start_date, R.end_date end_date
        FROM Reservations R LEFT JOIN Users U
        WHERE R.id = ?
    """, [reservation_id])[0]
                    

def get_post_reservations(post_id: int, start_date: str = "", end_date: str = ""):
    if start_date and end_date:
        return db.query("""
            SELECT R.id id, R.post post, R.user user_id, U.username username, R.start_date start_date, R.end_date end_date
            FROM Reservations R LEFT JOIN Users U ON R.user = U.id
            WHERE post = ? AND start_date <= ? AND end_date >= ?
            ORDER BY start_date
        """, [post_id, end_date, start_date])
    elif start_date:
        return db.query("""
            SELECT R.id id, R.post post, R.user user_id, U.username username, R.start_date start_date, R.end_date end_date
            FROM Reservations R LEFT JOIN Users U ON R.user = U.id
            WHERE post = ? AND end_date >= ?
            ORDER BY start_date
        """, [post_id, start_date])
    else:
        return db.query("""
            SELECT R.id id, R.post post, R.user user_id, U.username username, R.start_date start_date, R.end_date end_date
            FROM Reservations R LEFT JOIN Users U ON R.user = U.id
            WHERE post = ?
            ORDER BY start_date
        """, [post_id])


def add_reservation(post_id: int, user_id: int, start_date: str, end_date: str):
    return db.execute(
        "INSERT INTO Reservations (post, user, start_date, end_date) VALUES (?, ?, ?, ?)",
        [post_id, user_id, start_date, end_date]
    )

def remove_reservation(reservation_id: int):
    db.execute("DELETE FROM Reservations WHERE id = ?", [reservation_id])
