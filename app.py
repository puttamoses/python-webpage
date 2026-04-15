from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import random
import json
import os

app = Flask(__name__)
app.secret_key = "car-puzzle-secret-2024"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

CARS = [
    {"id": 1, "name": "Ferrari 488",   "speed": 330, "price": 250000, "color": "#e63946"},
    {"id": 2, "name": "Lamborghini Huracán", "speed": 325, "price": 230000, "color": "#f4a261"},
    {"id": 3, "name": "Porsche 911",   "speed": 310, "price": 120000, "color": "#2a9d8f"},
    {"id": 4, "name": "McLaren 720S",  "speed": 341, "price": 300000, "color": "#e9c46a"},
    {"id": 5, "name": "Bugatti Chiron","speed": 420, "price": 3000000,"color": "#264653"},
    {"id": 6, "name": "Aston Martin DB11","speed": 301,"price": 200000,"color": "#9b2226"},
]

# In-memory leaderboard
leaderboard: list[dict] = []


def sorted_cars(mode: str) -> list[dict]:
    if mode == "speed":
        return sorted(CARS, key=lambda c: c["speed"])
    elif mode == "price":
        return sorted(CARS, key=lambda c: c["price"])
    else:  # name
        return sorted(CARS, key=lambda c: c["name"])


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return redirect(url_for("game"))


@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "POST":
        action = request.args.get("action") or request.form.get("action", "")

        if action == "shuffle":
            mode = request.args.get("mode", "speed")
            shuffled = CARS.copy()
            random.shuffle(shuffled)
            session["mode"] = mode
            session["moves"] = 0
            return render_template("game.html", cars=shuffled, mode=mode, message=None, won=False)

        if action == "validate":
            data = request.get_json(silent=True) or {}
            order_ids = data.get("order", [])
            mode = session.get("mode", "speed")
            moves = session.get("moves", 0) + 1
            session["moves"] = moves

            correct_order = [c["id"] for c in sorted_cars(mode)]
            if order_ids == correct_order:
                score = max(100 - (moves - len(CARS)) * 5, 10)
                return jsonify({"correct": True, "score": score, "moves": moves})
            else:
                return jsonify({"correct": False, "moves": moves})

    # GET — start fresh
    mode = request.args.get("mode", "speed")
    shuffled = CARS.copy()
    random.shuffle(shuffled)
    session["mode"] = mode
    session["moves"] = 0
    return render_template("game.html", cars=shuffled, mode=mode, message=None, won=False)


@app.route("/api/score", methods=["GET", "POST"])
def score():
    global leaderboard
    if request.method == "GET":
        top10 = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
        return jsonify(top10)

    data = request.get_json(silent=True) or {}
    name  = data.get("name", "Anonymous")[:30]
    score_val = int(data.get("score", 0))
    mode  = data.get("mode", "speed")
    leaderboard.append({"name": name, "score": score_val, "mode": mode})
    return jsonify({"status": "ok"}), 201


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=8080)
