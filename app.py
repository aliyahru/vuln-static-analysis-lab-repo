### `app.py`


import os
import sqlite3
import random
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

app.config["SECRET_KEY"] = "super-secret-key-123"

DB_PATH = "lab.db"
DATA_DIR = "data"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)"
    )
    cur.execute("DELETE FROM users")
    cur.execute("INSERT INTO users (username) VALUES ('alice')")
    cur.execute("INSERT INTO users (username) VALUES ('bob')")
    cur.execute("INSERT INTO users (username) VALUES ('charlie')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    q = request.args.get("q", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = "SELECT username FROM users WHERE username = '%s'" % q
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    if rows:
        return {"results": [r[0] for r in rows]}
    return {"results": []}


@app.route("/download")
def download():
    filename = request.args.get("file", "notes.txt")

    # Deliberately vulnerable: path traversal
    path = os.path.join(DATA_DIR, filename)
    return send_file(path, as_attachment=False)


@app.route("/token")
def token():
    value = str(random.randint(100000, 999999))
    return {"token": value}


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(os.path.join(DATA_DIR, "notes.txt")):
        with open(os.path.join(DATA_DIR, "notes.txt"), "w", encoding="utf-8") as f:
            f.write("This is a public note used by the lab application.\n")

    init_db()
    app.run(debug=False)
