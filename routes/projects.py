from fastapi import APIRouter, Depends, Security, HTTPException
from schemas.projects import Project
from db.config import db_client

router = APIRouter(prefix='/api/projects', tags=['Projects'])


@router.get('/', status_code=200)
async def get_projects():
    projects = db_client.test.projects.find()
    if (not projects):
        raise HTTPException(
            status_code=400, detail='No hay proyectos en la base de datos')
    return {projects}


@router.post('/', status_code=201)
async def new_project(project_details: Project):
    if db_client.test.projects.find_one({"title": project_details.title}):
        raise HTTPException(
            status_code=400, detail="Ya existe un proyecto con ese titulo!")
    url_git = []
    for url in project_details.urlGit:
        url_dic = {"label": url.label, "url": url.url}
        url_git.append(url_dic)
    db_client.test.project.insert_one({"title": project_details.title, "description": project_details.description, "secDescription": project_details.secDescription,
                                      "technolofies": project_details.technologies, "ulrGit": url_git, "image": project_details.image, "author": project_details.author})
    return {"message": "Listorti"}
