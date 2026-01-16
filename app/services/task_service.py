from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate
from fastapi import HTTPException
from app.models.task import TaskStatus

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, task_in: TaskCreate, owner_id: int):
        return await self.repo.create(task_in, owner_id)
    
    async def get_tasks(self, owner_id: int, status=None, priority=None):
        return await self.repo.get_multi(owner_id, status, priority)
    

    async def block_task(self, task_id: int, blocker_id: int, user_id: int):
            task = await self.repo.get_with_blockers(task_id, user_id)
            
            blocker = await self.repo.get_by_id(blocker_id, user_id)

            if not task or not blocker:
                raise HTTPException(status_code=404, detail="Task not found")
            
            await self.repo.add_dependency(task, blocker)
            return {"message": f"Task {task_id} is now blocked by Task {blocker_id}"}

    async def update_task_status(self, task_id: int, new_status: TaskStatus, user_id: int):
        task = await self.repo.get_with_blockers(task_id, user_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if new_status == TaskStatus.DONE:
            for blocker in task.blocking_tasks:
                if blocker.status != TaskStatus.DONE:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Cannot complete task. It is blocked by Task {blocker.id} (Status: {blocker.status})"
                    )

        return await self.repo.update_status(task, new_status)