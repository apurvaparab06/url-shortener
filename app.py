import sqlite3, string, random
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
DB = "urls.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS urls (
            code TEXT PRIMARY KEY,
            long_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )""")

def make_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = (request.get_json() or {}).get("url", "")
    if not long_url.startswith(("http://", "https://")):
        return jsonify(error="Provide a valid http(s) URL"), 400
    with get_db() as conn:
        while True:
            code = make_code()
            exists = conn.execute("SELECT 1 FROM urls WHERE code = ?", (code,)).fetchone()
            if not exists:
                break
        conn.execute("INSERT INTO urls (code, long_url) VALUES (?, ?)", (code, long_url))
    return jsonify(short_url=request.host_url + code), 201

@app.route("/<code>")
def go(code):
    with get_db() as conn:
        row = conn.execute("SELECT long_url FROM urls WHERE code = ?", (code,)).fetchone()
        if not row:
            return jsonify(error="Not found"), 404
        conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE code = ?", (code,))
    return redirect(row["long_url"])

@app.route("/stats/<code>")
def stats(code):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM urls WHERE code = ?", (code,)).fetchone()
    if not row:
        return jsonify(error="Not found"), 404
    return jsonify(dict(row))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)