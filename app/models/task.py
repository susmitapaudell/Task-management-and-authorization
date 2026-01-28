from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    is_deleted = Column(Boolean, default=False)  # Soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="tasks")