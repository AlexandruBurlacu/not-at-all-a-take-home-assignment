from fastapi import FastAPI, status
from pydantic import BaseModel

import uuid

app = FastAPI()

class Blogpost(BaseModel):
    title: str
    paragraphs: list[str]

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_blogpost(blogpost: Blogpost) -> dict[str, str]:
    slug = blogpost.title.lower().replace(" ", "-") + f"-{uuid.uuid4()}"
    return {"blogpost_slug": slug}
