from schemas.projects import Project
from .config import db_client


async def get_all_projects():
    projects = []
    cursos = db_client.test.project.find({})
    async for doc in cursos:
        print(doc)
        projects.append(Project(**doc))
    return projects


async def create_project(project):
    new_project = await db_client.test.project.insert_one(project)
    print(new_project)
    created_project = await db_client.test.project.find_one({'_id': new_project.inserted_id})
    return created_project
