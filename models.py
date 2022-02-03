from pydantic import BaseModel


class Blogpost(BaseModel):
    title: str
    paragraphs: list[str]
    slug: str
    blogpost_id: str
    has_foul_language: bool | None = None


class BlogpostRequest(BaseModel):
    title: str
    paragraphs: list[str]


class BlogpostResponse(BaseModel):
    blogpost_slug: str
