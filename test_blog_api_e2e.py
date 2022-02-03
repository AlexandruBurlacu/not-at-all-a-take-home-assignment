from fastapi.testclient import TestClient
import pytest

from blog_api import app


@pytest.fixture
def fastapi_client():
    client = TestClient(app)
    return client


def test_blog_posting_ok(fastapi_client):
    resp = fastapi_client.post("/posts", headers={
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


def test_blog_posting_trailing_whitespace(fastapi_client):
    resp = fastapi_client.post("/posts", headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    }, json={
        "title": "  Dummy Title   ",
        "paragraphs": [
            "Paragraph 1",
            "Paragraph two",
            "Final paragraph"
        ]
    })


    assert resp.status_code == 201
    assert not resp.json().get("blogpost_slug").startswith("dummy-title--")
    assert not resp.json().get("blogpost_slug").startswith("--dummy-title--")
    assert not resp.json().get("blogpost_slug").startswith("  dummy-title--")
    assert not resp.json().get("blogpost_slug").startswith("dummy-title- ")
    assert resp.json().get("blogpost_slug").startswith("dummy-title-")