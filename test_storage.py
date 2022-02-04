import uuid
from src.storage import fetch_blogpost, insert_blogpost, update_blogpost

import pytest


def test_insert_blogpost_ok():
    title = "a title"
    slug = "a-slug-12af-1234-ababaff"
    paragraphs = ["one", "two", "three and four"]
    blogpost_id = insert_blogpost(title, slug, paragraphs)

    assert blogpost_id is not None

    blogpost = fetch_blogpost(blogpost_id)

    assert blogpost.title == title
    assert blogpost.slug == slug
    assert blogpost.paragraphs == paragraphs

    assert blogpost.has_foul_language is None


def test_fetch_blogpost_not_ok():
    blogpost_id = "3a4f-12af-1234-dbabaff"

    with pytest.raises(KeyError):
        blogpost = fetch_blogpost(blogpost_id)


def test_update_blogpost_ok():
    title = "a title"
    slug = "a-slug-12af-1234-ababaff"
    paragraphs = ["one", "two", "three and four"]
    blogpost_id = insert_blogpost(title, slug, paragraphs)

    update_blogpost(blogpost_id, True)
    # if it doesn't die, it works


def test_update_blogpost_not_ok():
    blogpost_id = str(uuid.uuid4())
    with pytest.raises(KeyError):
        update_blogpost(blogpost_id, False)