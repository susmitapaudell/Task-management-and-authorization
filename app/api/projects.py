# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.deps import get_db, get_current_user, require_admin, get_owned_project
# from app.models.project import Project
# from app.models.user import User

# router = APIRouter(prefix="/projects", tags=["projects"])

# @router.post("/projects")
# def create_project(
#     name: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     project = Project(
#         name=name,
#         owner_id=current_user.id
#     )
#     db.add(project)
#     db.commit()
#     db.refresh(project)
#     return project

# @router.get("/")
# def list_projects(
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user)
# ):
#     if user.is_admin:
#         return db.query(Project).all()

#     return db.query(Project).filter(Project.owner_id == user.id).all()

# @router.delete("/{project_id}")
# def delete_project(
#     project_id: int,
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user)
# ):
#     project = db.query(Project).filter(Project.id == project_id).first()
#     if not project:
#         raise HTTPException(404, "Project not found")

#     if not (user.is_admin or project.owner_id == user.id):
#         raise HTTPException(403, "Not authorized")

#     db.delete(project)
#     db.commit()

#     return {"msg": "Deleted"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.core.deps import get_current_user, get_owned_project

router = APIRouter(prefix="/projects", tags=["projects"])

# CREATE
@router.post("/", response_model=ProjectOut)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = Project(**project_in.dict(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

# LIST OWNED
@router.get("/", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Project).filter(
        Project.owner_id == current_user.id,
        Project.deleted_at.is_(None)
    ).all()

# GET SINGLE
@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project: Project = Depends(get_owned_project)
):
    return project

# UPDATE
@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_in: ProjectUpdate,
    project: Project = Depends(get_owned_project),
    db: Session = Depends(get_db)
):
    for field, value in project_in.dict(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project

# DELETE (soft)
@router.delete("/{project_id}")
def delete_project(
    project: Project = Depends(get_owned_project),
    db: Session = Depends(get_db)
):
    project.deleted_at = func.now()
    db.commit()
    return {"detail": "Project deleted"}
