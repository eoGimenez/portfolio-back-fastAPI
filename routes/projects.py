from fastapi import APIRouter, Depends, Security, HTTPException
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from schemas.projects import Project
from db.config import db_client

router = APIRouter(prefix='/api/projects', tags=['Projects'])


@router.get('/', status_code=200)
async def get_projects():
    projects_list = []
    projects_db = db_client.test.project.find()
    if (not projects_db):
        raise HTTPException(
            status_code=400, detail='No hay proyectos en la base de datos')
    for x in projects_db:
        aux_project = Project(**x)
        aux_project.id = str(x["_id"])
        projects_list.append(aux_project)
    return projects_list


@router.post('/', status_code=201)
async def new_project(project_details: Project):
    if db_client.test.projects.find_one({"title": project_details.title}):
        raise HTTPException(
            status_code=400, detail="Ya existe un proyecto con ese titulo!")
    url_git = []
    for url in project_details.urlGit:
        url_dic = {"label": url["label"], "url": url["url"]}
        url_git.append(url_dic)
    db_client.test.project.insert_one({"title": project_details.title, "description": project_details.description, "secDescription": project_details.secDescription,
                                      "technologies": project_details.technologies, "urlGit": url_git, "image": project_details.image, "author": project_details.author})
    return {"message": "Listorti"}


@router.put('/{id}', status_code=200)
async def update_project(id: str, updated_data: Project):
    project_id = ObjectId(id)
    project_to_update: Project = db_client.test.project.find_one_and_update(
        {"_id": project_id}, {"$set": updated_data.dict()}, return_document=ReturnDocument.AFTER)
    return {"_id": str(project_id), "title": project_to_update["title"], "description": project_to_update["description"], "secDescription": project_to_update["secDescription"], "technologies": project_to_update["technologies"], "urlGit": project_to_update["urlGit"], "image": project_to_update["image"], "author": project_to_update["author"]}
