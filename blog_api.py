from fastapi import FastAPI, status

from src.models import BlogpostRequest, BlogpostResponse

from src.ml_service_client import FoulLanguageDetector
from src.storage import insert_blogpost

from src.mocked_requests import requests

import uuid

app = FastAPI()

detector = FoulLanguageDetector(requests)


def prepare_slug_prefix(title: str):
    return title.lower().rstrip(" ").lstrip(" ").replace(" ", "-")


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=BlogpostResponse)
def post_blogpost(blogpost: BlogpostRequest) -> BlogpostResponse:
    slug = prepare_slug_prefix(blogpost.title) + f"-{uuid.uuid4()}"
    blogpost_id = insert_blogpost(blogpost.title, slug, blogpost.paragraphs)
    detector.detect_foul_language(blogpost_id)
    return BlogpostResponse(blogpost_slug=slug)
