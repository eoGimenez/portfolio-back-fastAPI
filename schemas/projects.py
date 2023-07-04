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
    image: Optional[HttpUrl]
    author: Optional[dict]


# def project_schema(projects) -> list:
#     return [project == Project(**project) for project in projects]


""" 
PARA ENVIAR PETICIONES DE PRUEBA A LA API

{
    "title": "test",
    "description": "descripcion",
    "secDescription": "segunda des",
    "technologies": ["PROBANDO", "QUE ONDA", "akka"],
    "urlGit": [
      {
       "label": "titulo aaaaaaaaaaaimagen",
       "url": "https://www.google.com"
        
      },
         {
       "label": "titul SEGUssssssssNDA imagen",
       "url": "https://www.youtube.com"
        
      }
        ],
    "image": "https://res.cloudinary.com/dbld4vcec/image/upload/v1685561602/projects/vab1fxizdea2tryposca.png",
    "author": {"email": "Eugeni"}
} """
