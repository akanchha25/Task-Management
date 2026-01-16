from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.core.config import settings
from app.core import security
from app.models.user import User
from app.schemas.token import TokenPayload
from sqlalchemy import select

# 1. Setup OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode Token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id)
    except JWTError:
        raise credentials_exception
        
    # Fetch User from DB
    result = await db.execute(select(User).where(User.id == int(token_data.sub)))
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
    return user