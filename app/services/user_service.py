from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, user_in: UserCreate):
        # 1. Check if user already exists
        existing_user = await self.repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        # 2. Create new user
        return await self.repo.create(user_in)