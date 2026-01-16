from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema with shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return via API (Never return the password!)
class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models