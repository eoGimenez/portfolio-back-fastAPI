from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from bson import ObjectId
from bson.objectid import ObjectId
# from .user import User


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, var):
        if not ObjectId.is_valid(var):
            raise ValueError("ObjectId Invalido")
        return ObjectId(var)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UrlGit(BaseModel):
    label: str
    url: HttpUrl


class Project(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    secDescription: str
    technologies: list[str] = Field(default_factory=list)
    urlGit: list[dict] = Field(default_factory=list)
    image: Optional[HttpUrl]
    author: Optional[dict]


# def project_schema(projects) -> list:
#     return [project == Project(**project) for project in projects]


""" {
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
