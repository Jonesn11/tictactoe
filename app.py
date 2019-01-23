
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
 
app = Flask(__name__)
 
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None
    return render_template("game.html", game=session["board"], turn=session["turn"])
 
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    if session["turn"] == 'X':
        session["turn"] = 'O'
    elif session["turn"] == 'O':
        session["turn"] = 'X'
    if any([(all(i == 'X' for i in x)) for x in session["board"]]) or any([(all(i == 'X' for i in x)) for x in list(zip(*session["board"]))]):
        session["winner"] = 'X'
        return redirect("/win")
    elif any([(all(i == 'O' for i in x)) for x in session["board"]]) or any([(all(i == 'O' for i in x)) for x in list(zip(*session["board"]))]):
        session["winner"] = 'O'
        return redirect("/win")
    return redirect(url_for("index"))

@app.route("/win")
def win():
    winner = session["winner"]
    return render_template("win.html", winner=winner)




# Using technology to connect people in a meaningful and safe way, there is periscope