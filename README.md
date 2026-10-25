# URL Shortener

A simple URL shortener built with Flask and SQLite.

## Features
- Shorten any http(s) URL into a 6-character code
- Redirect from the short link to the original URL
- Click counting for each link
- Stats endpoint
- Input validation and duplicate-code handling
- Automated tests with pytest

## Tech Stack
Python, Flask, SQLite, pytest

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
```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/shorten -ContentType "application/json" -Body '{"url": "https://github.com"}'
```

## Run tests
```bash
pytest
```