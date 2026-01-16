from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_data: TaskCreate, owner_id: int) -> Task:
        # Convert Pydantic model to DB model
        db_task = Task(
            **task_data.model_dump(),
            owner_id=owner_id
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task
    

    async def get_multi(
        self, 
        owner_id: int, 
        status: Optional[TaskStatus] = None,
        priority: Optional[int] = None
    ) -> List[Task]:
        # Start with a base query: "Select all tasks owned by this user"
        query = select(Task).where(Task.owner_id == owner_id)
        
        # Dynamically add filters if they are provided
        if status:
            query = query.where(Task.status == status)
        
        if priority:
            query = query.where(Task.priority == priority)
            
        # Execute query
        result = await self.db.execute(query)
        return result.scalars().all()


    async def get_by_id(self, task_id: int, owner_id: int) -> Optional[Task]:
        query = select(Task).where(
            and_(Task.id == task_id, Task.owner_id == owner_id)
        )
        result = await self.db.execute(query)
        return result.scalars().first()
    

    async def get_with_blockers(self, task_id: int, owner_id: int) -> Optional[Task]:
            query = select(Task).options(
                selectinload(Task.blocking_tasks)
            ).where(
                and_(Task.id == task_id, Task.owner_id == owner_id)
            )
            result = await self.db.execute(query)
            return result.scalars().first()
    

    async def add_dependency(self, blocked_task: Task, blocker_task: Task):
        blocked_task.blocking_tasks.append(blocker_task)
        await self.db.commit()
        await self.db.refresh(blocked_task)

    async def update_status(self, task: Task, new_status: TaskStatus):
        task.status = new_status
        await self.db.commit()
        await self.db.refresh(task)
        return task