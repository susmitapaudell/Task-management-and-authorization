from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, get_current_admin
from app.models.project import Project
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/")
def list_projects(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if user.is_admin:
        return db.query(Project).all()

    return db.query(Project).filter(Project.owner_id == user.id).all()

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")

    if not (user.is_admin or project.owner_id == user.id):
        raise HTTPException(403, "Not authorized")

    db.delete(project)
    db.commit()
    return {"msg": "Deleted"}
