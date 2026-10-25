import sqlite3, string, random
from flask import Flask, request, redirect, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
DB = "urls.db"

# NEW: the HTML for the home page
HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>URL Shortener</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 520px; margin: 80px auto; padding: 0 16px; color: #222; }
  h1 { margin-bottom: 4px; }
  p.sub { color: #666; margin-top: 0; }
  input { width: 100%; padding: 12px; font-size: 16px; box-sizing: border-box; border: 1px solid #bbb; border-radius: 6px; }
  button { margin-top: 12px; padding: 12px 20px; font-size: 16px; border: 0; border-radius: 6px; background: #2563eb; color: #fff; cursor: pointer; }
  button:hover { background: #1d4ed8; }
  #result { margin-top: 20px; font-size: 18px; word-break: break-all; }
  .error { color: #b91c1c; }
</style>
</head>
<body>
<h1>URL Shortener</h1>
<p class="sub">Paste a long link and get a short one.</p>
<input id="url" type="url" placeholder="https://example.com/very/long/link">
<button id="btn">Shorten</button>
<p id="result"></p>
<script>
document.getElementById("btn").addEventListener("click", async () => {
  const result = document.getElementById("result");
  const url = document.getElementById("url").value.trim();
  result.className = "";
  result.textContent = "Working...";
  try {
    const res = await fetch("/shorten", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    if (res.ok) {
      result.textContent = "";
      const a = document.createElement("a");
      a.href = data.short_url;
      a.textContent = data.short_url;
      a.target = "_blank";
      result.appendChild(a);
    } else {
      result.className = "error";
      result.textContent = data.error || "Something went wrong";
    }
  } catch (e) {
    result.className = "error";
    result.textContent = "Network error. Try again.";
  }
});
</script>
</body>
</html>"""

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

# NEW: home page route
@app.route("/")
def home():
    return HOME_HTML

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

init_db()

if __name__ == "__main__":
    app.run(debug=True)