from datetime import datetime

from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route("/")
def index():
    db.execute("INSERT INTO Visits (visited_at) VALUES (datetime('now'))")
    visit_count = db.query("SELECT COUNT(*) AS c FROM Visits")[0]["c"]
    return render_template("index.html", visit_count=visit_count)