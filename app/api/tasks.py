# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from sqlalchemy.sql import func

# from app.core.deps import get_db, get_current_user, get_owned_project, get_owned_task
# from app.models.task import Task
# from app.models.project import Project

# router = APIRouter(tags=["tasks"])

# @router.post("/projects/{project_id}/tasks")
# def create_task(
#     title: str,
#     project: Project = Depends(get_owned_project),
#     db: Session = Depends(get_db),
# ):
#     task = Task(
#         title=title,
#         project_id=project.id
#     )

#     db.add(task)
#     db.commit()
#     db.refresh(task)

#     return task

# @router.get("/tasks/{task_id}")
# def get_task(
#     task=Depends(get_owned_task)
# ):
#     return task

# @router.delete("/tasks/{task_id}")
# def delete_task(
#     task=Depends(get_owned_task),
#     db: Session = Depends(get_db)
# ):
#     task.deleted_at = func.now()
#     db.commit()
#     return {"detail": "Task deleted"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.core.deps import get_current_user, get_owned_project, get_owned_task

router = APIRouter(prefix="/tasks", tags=["tasks"])

# CREATE task inside project
@router.post("/projects/{project_id}", response_model=TaskOut)
def create_task(
    task_in: TaskCreate,
    project=Depends(get_owned_project),
    db: Session = Depends(get_db)
):
    task = Task(**task_in.dict(), project_id=project.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# LIST tasks in a project
@router.get("/projects/{project_id}", response_model=list[TaskOut])
def list_tasks(
    project=Depends(get_owned_project),
    db: Session = Depends(get_db)
):
    return db.query(Task).filter(
        Task.project_id == project.id,
        Task.deleted_at.is_(None)
    ).all()

# GET single task
@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task=Depends(get_owned_task)
):
    return task

# UPDATE task
@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_in: TaskUpdate,
    task=Depends(get_owned_task),
    db: Session = Depends(get_db)
):
    for field, value in task_in.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

# DELETE task (soft)
@router.delete("/{task_id}")
def delete_task(
    task=Depends(get_owned_task),
    db: Session = Depends(get_db)
):
    task.deleted_at = func.now()
    db.commit()
    return {"detail": "Task deleted"}
