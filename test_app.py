from app import app, init_db

def test_shorten_and_redirect():
    init_db()
    client = app.test_client()
    res = client.post("/shorten", json={"url": "https://example.com"})
    assert res.status_code == 201
    code = res.get_json()["short_url"].split("/")[-1]
    assert client.get(f"/{code}").status_code == 302

def test_invalid_url():
    client = app.test_client()
    res = client.post("/shorten", json={"url": "nope"})
    assert res.status_code == 400

def test_not_found():
    init_db()
    client = app.test_client()
    res = client.get("/doesnotexist")
    assert res.status_code == 404