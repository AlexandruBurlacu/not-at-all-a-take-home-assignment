from models import Blogpost

import uuid

my_dummy_db: dict[str, Blogpost] = dict()


def insert_blogpost(title: str, slug: str, paragraphs: list[str]) -> str:
    blogpost_id = str(uuid.uuid4())
    if not my_dummy_db.get(blogpost_id):
        my_dummy_db[blogpost_id] = Blogpost(blogpost_id=blogpost_id, title=title, slug=slug, paragraphs=paragraphs)
    else:
        blogpost_id = str(uuid.uuid4())
        my_dummy_db[blogpost_id] = Blogpost(blogpost_id=blogpost_id, title=title, slug=slug, paragraphs=paragraphs)
    return blogpost_id


def fetch_blogpost(blogpost_id: str) -> Blogpost:
    if blogpost := my_dummy_db.get(blogpost_id):
        return blogpost
    else:
        raise KeyError(f"Blogpost with id {blogpost_id} doesn't exist")


def update_blogpost(blogpost_id: str, has_foul_language: bool):
    if blogpost := my_dummy_db.get(blogpost_id):
        blogpost.has_foul_language = has_foul_language
    else:
        raise KeyError(f"Blogpost with id {blogpost_id} doesn't exist")
