from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class UrlGit(BaseModel):
    label: str
    url: HttpUrl


class Project(BaseModel):
    id: Optional[str] | None = None
    title: str
    description: str
    secDescription: str
    technologies: list[str] = Field(default_factory=list)
    urlGit: list[dict] = Field(default_factory=list)
    image: Optional[str]
    author: Optional[dict]
