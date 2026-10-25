# URL Shortener

A simple URL shortener built with Flask and SQLite.

**Live demo:** https://url-shortener-vb0t.onrender.com

> Hosted on Render's free tier, so the first request after a period of inactivity can take 30 to 60 seconds. Saved links may reset when the server restarts.

## Features
- Shorten any http(s) URL into a 6-character code
- Redirect from the short link to the original URL
- Click counting for each link
- Stats endpoint
- Input validation and duplicate-code handling
- Automated tests with pytest
- Deployed with Gunicorn on Render

## Tech Stack
Python, Flask, SQLite, Gunicorn, pytest

## Setup
```bash
git clone https://github.com/apurvaparab06/url-shortener.git
cd url-shortener
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/shorten` | Create a short link. Body: `{"url": "https://example.com"}` |
| GET | `/<code>` | Redirect to the original URL and count the click |
| GET | `/stats/<code>` | Show the original URL and click count |

## Example
Create a short link on the live app:

```powershell
Invoke-RestMethod -Method Post -Uri https://url-shortener-vb0t.onrender.com/shorten -ContentType "application/json" -Body '{"url": "https://github.com"}'
```

Response:

```json
{"short_url": "https://url-shortener-vb0t.onrender.com/Ab12Cd"}
```

Open the short link in a browser to be redirected, or visit `/stats/Ab12Cd` to see the click count.

## Run tests
```bash
pytest
```