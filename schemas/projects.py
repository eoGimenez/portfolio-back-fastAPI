from pydantic import BaseModel, HttpUrl
from .user import User


class UrlGit(BaseModel):
    label: str
    url: HttpUrl


class Project(BaseModel):
    title: str
    description: str
    secDescription: str
    technologies: list
    urlGit: list[UrlGit]
    image: HttpUrl | None = None
    # author: set = User


""" {
    "title": "test",
    "description": "descripcion",
    "secDescription": "segunda des",
    "technologies": ["test1", "testw", "akka"],
    "urlGit": [
      {
       "label": "titulo imagen",
       "url": "https://www.google.com"
        
      },
         {
       "label": "titul SEGUNDA imagen",
       "url": "https://www.youtube.com"
        
      }
        ],
    "image": "https://res.cloudinary.com/dbld4vcec/image/upload/v1685561602/projects/vab1fxizdea2tryposca.png"
} """
