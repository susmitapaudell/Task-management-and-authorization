from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.project import Project
from app.models.task import Task
