import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, flash, session
from datetime import datetime
from flask_session import Session
from functools import wraps

# Configure app to work with Flask
app = Flask(__name__)

# App configuration for sessions and more
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "f7237b99bdec421188be92fb042a36e6"
Session(app)

# Configure database
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)


def join_required(f):
    """Decorate routes to require joining."""

    # https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/join")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/join", methods=["GET", "POST"])
def join():
    """Allow user to enter the site"""

    # Forget any user id
    session.clear()

    # User reached via POST (submitting a form)
    if request.method == "POST":
        email = request.form.get("email")

        # Ensure email meets requirements
        if not email or not "asdubai.org" in email:
            return redirect("/join")

        # Creating user and user_id to be used in all other routes
        record = db.execute("SELECT * FROM students WHERE email = ?", email)
        if len(record) == 0:
            db.execute("INSERT INTO STUDENTS (email) VALUES(?)", email)

        session["user_id"] = db.execute("SELECT id FROM students WHERE email = ?", email)[0]["id"]
        flash("Successful!")
        return redirect("/")

    # User reached via GET (link or redirect)
    return render_template("join.html")


@app.route("/")
@join_required
def index():
    """Load home page for user to choose a scale"""

    return render_template("index.html")


@app.route("/scales", methods=["GET", "POST"])
@join_required
def scales():
    """Load home page for user to choose a scale"""

    # User reached via GET (link or redirect)
    if request.method == "GET":
        return redirect("/")

    # User reached via POST (submitting a form)
    scaleName = request.form.get("scale")
    clef = request.form.get("clef")

    # Ensure user picked scale and clef before submitting
    if not scaleName or not clef:
        flash("Please fill out all fields before submitting!")
        return redirect("/")

    # 12 notes to display based on scale
    octaves = {
        "C-major": ["C4", "Db4", "D4", "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4", "C5"],
        "F-major": ["F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4", "Eb4", "E4", "F4"],
        "Bb-major": ["Bb3", "B3", "C4", "Db4", "D4", "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4"],
        "Eb-major": ["Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4", "Eb4"],
    }

    # Correct notes part of the scale
    scales = {
        "C-major": ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"],
        "F-major": ["F3", "G3", "A3", "Bb3", "C4", "D4", "E4", "F4"],
        "Bb-major": ["Bb3", "C4", "D4", "Eb4", "F4", "G4", "A4", "Bb4"],
        "Eb-major": ["Eb3", "F3", "G3", "Ab3", "Bb3", "C4", "D4", "Eb4"],
    }

    # Take user to page to attempt the scale
    return render_template("scales.html", scaleName=scaleName, clef=clef, octave=octaves[scaleName], scale=scales[scaleName])


@app.route("/save_scores", methods=["GET", "POST"])
@join_required
def save():
    """Save user's score and add it to leaderboard"""

    # User reached via GET (link or redirect)
    if request.method == "GET":
        return redirect("/")

    # User reached via POST (submitting a form)
    scale = request.form.get("scale")
    score = request.form.get("score")
    email = db.execute("SELECT email FROM students WHERE id = ?", session["user_id"])[0]["email"]

    # Ensure user filled in name and score
    if not score:
        flash("Please attempt the scale before saving!")
        return redirect("/")

    dt = datetime.now().strftime("%Y-%m-%d")

    # Insert user's score into leaderboard table
    record = db.execute("SELECT COUNT(1) AS count FROM leaderboard WHERE name = ? AND scale = ?", email[:-15], scale)[0]["count"]
    if record == 0:
        db.execute("INSERT INTO leaderboard (name, scale, score, datetime) VALUES(?, ?, ?, ?)", email[:-15], scale, score, dt)
    else:
        db.execute("UPDATE leaderboard SET score = ? WHERE name = ? AND scale = ?", score, email[:-15], scale)

    # Take user to home page
    flash("Your score has been saved. Check to see if it's on the leaderboard!")
    return redirect("/")


@app.route("/leaderboard", methods=["GET", "POST"])
@join_required
def leaderboard():
    """Display leaderboard corresponding to chosen scale"""

    # User reached via POST (submitting a form)
    if request.method == "POST":
        scale = request.form.get("scale")

        # Ensure user picked scale before submitting
        if not scale:
            flash("Please choose a scale to display!")
            return redirect("/leaderboard")

        # Find top 30 scores from given scale
        leaderboard = db.execute("SELECT name, score, datetime FROM leaderboard WHERE scale = ? ORDER BY score DESC LIMIT 30", scale)
        return render_template("leaderboard.html", leaderboard=leaderboard)

    # User reached via GET (link or redirect)
    return render_template("leaderboard.html", leaderboard=None)