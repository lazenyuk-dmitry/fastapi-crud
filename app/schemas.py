from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

UserName = Annotated[str, Field(..., min_length=2, max_length=50)]
UserPassword = Annotated[str, Field(min_length=8)]

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    name: UserName
    email: EmailStr
    role: UserRole = UserRole.USER
    is_active: bool = True

class UserCreate(UserBase):
    password: UserPassword

class UserUpdate(UserBase):
    name: Optional[UserName] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    role: Optional[bool] = None

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class AuthUser(BaseModel):
    user: User
    access_token: str
    token_type: str

class AppResult(BaseModel):
    message: str
