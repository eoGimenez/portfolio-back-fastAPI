from pydantic import BaseModel, HttpUrl
from .user import User


class UrlGit(BaseModel):
    label: str
    url: str


class Project(BaseModel):
    title: str
    description: str
    secDescription: str
    technologies: list
    urlGit: list[UrlGit]
    image: HttpUrl | None = None
    # author: set = User
