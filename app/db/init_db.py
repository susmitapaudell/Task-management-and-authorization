from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.project import Project
from app.models.task import Task

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "main":
    init_db()