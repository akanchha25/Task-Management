from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.task import TaskCreate, TaskResponse, TaskStatus
from app.repositories.task_repo import TaskRepository
from app.services.task_service import TaskService
from app.models.user import User
from typing import List, Optional
from fastapi import Query

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new task. (Login required)
    """
    repo = TaskRepository(db)
    service = TaskService(repo)
    return await service.create_task(task_in, current_user.id)


@router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get tasks with optional filtering (Status, Priority).
    """
    repo = TaskRepository(db)
    service = TaskService(repo)
    return await service.get_tasks(current_user.id, status, priority)


@router.post("/{task_id}/dependencies/{blocker_id}")
async def add_dependency(
    task_id: int,
    blocker_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Make 'task_id' depend on 'blocker_id'.
    """
    repo = TaskRepository(db)
    service = TaskService(repo)
    return await service.block_task(task_id, blocker_id, current_user.id)


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_status(
    task_id: int,
    status: TaskStatus,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update task status. Checks for blockers if marking as DONE.
    """
    repo = TaskRepository(db)
    service = TaskService(repo)
    return await service.update_task_status(task_id, status, current_user.id)