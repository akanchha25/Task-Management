from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, user: UserCreate) -> User:
        # Hash the password
        hashed_password = get_password_hash(user.password)
        
        # Create DB Object
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            role="USER" # Default role
        )
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user