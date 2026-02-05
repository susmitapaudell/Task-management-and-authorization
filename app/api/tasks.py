from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, get_current_admin
from app.models.project import Project
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/projects/{project_id}/tasks")
def create_task(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(404, "Project not found")

    if not (user.is_admin or project.owner_id == user.id):
        raise HTTPException(403, "Not authorized")

    # create task here
