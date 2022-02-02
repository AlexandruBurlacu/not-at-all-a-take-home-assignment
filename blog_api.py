from fastapi import FastAPI, status
from pydantic import BaseModel

import uuid

app = FastAPI()

class Blogpost:
    class Request(BaseModel):
        title: str
        paragraphs: list[str]
    
    class Response(BaseModel):
        blogpost_slug: str


def prepare_slug_prefix(title: str):
    return title.lower().rstrip(" ").lstrip(" ").replace(" ", "-")


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Blogpost.Response)
def post_blogpost(blogpost: Blogpost.Request) -> Blogpost.Response:
    slug = prepare_slug_prefix(blogpost.title) + f"-{uuid.uuid4()}"
    return Blogpost.Response(blogpost_slug=slug)
