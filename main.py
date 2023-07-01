from fastapi import FastAPI
from routes import auth, projects

app = FastAPI()

app.include_router(auth.router)
app.include_router(projects.router)


@app.get("/")
async def root():
    return {"message": "Funciona"}
