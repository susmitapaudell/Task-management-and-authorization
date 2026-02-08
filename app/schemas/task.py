from pydantic import BaseModel, constr, Field
from typing import Optional, Literal
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = "todo"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None

class TaskOut(TaskBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_deleted: bool

    class Config:
        orm_mode = True
