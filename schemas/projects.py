from pydantic import BaseModel, HttpUrl
from .user import User


class UrlGit(BaseModel):
    label: str
    url: HttpUrl


class Project(BaseModel):
    title: str
    description: str
    secDescription: str
    technologies: set[str] = []
    urlGit: UrlGit = []
    image: HttpUrl
    author: set = User
