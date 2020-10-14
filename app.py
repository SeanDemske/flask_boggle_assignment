from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "SESSION_KEY"

boggle = Boggle()
gameboard = boggle.make_board()

@app.route("/")
def index():
    """Route for the index/homepage"""

    session["board"] = gameboard
    times_played = session.get("times_played", 0)
    highscore = session.get("highscore", 0)
    return render_template("index.html", gameboard=gameboard, highscore=highscore, times_played=times_played)

@app.route("/check-word")
def check_word():
    """Check if word is a valid and returns the status of the guessed word"""

    word = request.args["word"]
    res = boggle.check_valid_word(session["board"], word)
    return jsonify({"result": res})

@app.route("/end-game", methods=["POST"])
def end_game():
    """Update server data on endgame"""

    score = request.json["score"]
    times_played = session.get("times_played", 0)
    highscore = session.get("highscore", 0)


    session["highscore"] = max(score, highscore)
    session["times_played"] = times_played + 1

    json = {
        "timesPlayed": session["times_played"],
        "highscore": session["highscore"]
    }

    return jsonify(json)


