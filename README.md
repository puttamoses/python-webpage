# 🏎️ Car Ordering Puzzle — Python (Flask)

Interactive drag-and-drop car ordering puzzle, re-implemented in Python using Flask.

## Project Structure

```
python-car-puzzle/
├── app.py                  ← Flask application (routes + game logic)
├── requirements.txt        ← pip dependencies
├── templates/
│   └── game.html           ← Jinja2 template (game UI)
└── static/
    ├── css/style.css       ← Racing-theme stylesheet
    └── js/
        ├── drag.js         ← HTML5 + touch drag-and-drop
        └── fireworks.js    ← Win celebration animation
```

## Quick Start

```bash
cd python-car-puzzle

# Install dependencies
pip install -r requirements.txt

# Run dev server
python app.py
# → Open: http://localhost:8080
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET    | `/game` | Load game (shuffle cards) |
| POST   | `/game?action=shuffle&mode=speed` | New game with mode |
| POST   | `/game?action=validate` | Validate current order (JSON body: `{"order":[...]}`) |
| GET    | `/api/score` | Get top 10 scores (JSON) |
| POST   | `/api/score` | Submit score (JSON body: `{"name":"...","score":N,"mode":"..."}`) |

## Tech Stack

- **Python 3.10+** + **Flask 3.x**
- **Jinja2** templating (built-in to Flask)
- Vanilla **HTML5 / CSS3 / JavaScript** (no frontend framework)
- In-memory leaderboard (restart resets scores)
