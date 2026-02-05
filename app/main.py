from fastapi import FastAPI
from app.api import auth, projects, tasks

from app.models.user import User
from app.models.project import Project
from app.models.task import Task

app = FastAPI()


@app.get('/')
def home():
    return{"message" : "welcome to task db"}

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)



