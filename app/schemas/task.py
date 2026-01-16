from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum

# Helper Enum to match our Database Model
class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    DONE = "DONE"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 1
    due_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.TODO

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True