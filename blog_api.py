from fastapi import FastAPI, status
from pydantic import BaseModel

import uuid

app = FastAPI()

class Blogpost(BaseModel):
    title: str
    paragraphs: list[str]


def prepare_slug_prefix(title: str):
    return title.lower().rstrip(" ").lstrip(" ").replace(" ", "-")


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_blogpost(blogpost: Blogpost) -> dict[str, str]:
    slug = prepare_slug_prefix(blogpost.title) + f"-{uuid.uuid4()}"
    return {"blogpost_slug": slug}
