from fastapi.testclient import TestClient

from blog_api import app

client = TestClient(app)

def test_blog_posting_ok():
    resp = client.post("/posts", headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    }, json={
        "title": "Dummy Title",
        "paragraphs": [
            "Paragraph 1",
            "Paragraph two",
            "Final paragraph"
        ]
    })


    assert resp.status_code == 201
    assert resp.json().get("blogpost_slug").startswith("dummy-title-")