from fastapi import APIRouter, Depends, Security, HTTPException
from schemas.projects import Project, User
from db.config import db_client
from .auth import verify_token, AuthHandler

router = APIRouter(prefix='/api/projects', tags=['Projects'])

auth_handler = AuthHandler()


@router.get('/', status_code=200)
async def get_projects():
    projects = db_client.test.projects.find()
    if (not projects):
        raise HTTPException(
            status_code=400, detail='No hay proyectos en la base de datos')
    return {projects}


@router.post('/', status_code=201)
async def new_project(project_details: Project):
    user: User = verify_token(email=Depends(auth_handler.auth_wrapper))
    if db_client.test.projects.find_one({"title": project_details.title}):
        raise HTTPException(
            status_code=400, detail="Ya existe un proyecto con ese titulo!")
    db_client.test.project.insert_one({"title": project_details.title, "description": project_details.description, "secDescription": project_details.secDescription,
                                      "technolofies": project_details.technologies, "ulrGit": project_details.urlGit, "image": project_details.image, "author": user})
    return {"message": "Listorti"}
