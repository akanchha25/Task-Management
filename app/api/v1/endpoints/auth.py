from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps 
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from app.schemas.token import Token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_db) 
):
    """
    Register a new user.
    """
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.register_user(user_in)


@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(deps.get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    repo = UserRepository(db)
    user = await repo.get_by_email(form_data.username) # OAuth2 forms use 'username' for email
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=30)
    access_token = security.create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }