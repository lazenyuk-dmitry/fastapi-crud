from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from typing import Annotated
from app.database import get_db
from app.services.user_service import UserService
from app.models import UserORM
from app.schemas import UserRole
from app.config import settings
from app.exceptions import (
    OnlyForOwnerError,
    OnlyForAdminError,
    InvalidCredentialsError,
    InvalidTokenError
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> UserORM:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user = await user_service.get_by_email(email)

        if email is None:
            raise InvalidTokenError()
        return user
    except Exception:
        raise InvalidCredentialsError()

async def admin_only(user: UserORM = Depends(get_current_user)) -> UserORM:
    if user.role != UserRole.ADMIN:
        raise OnlyForAdminError()
    return user

async def admin_or_owner(
    user_id: int,
    current_user: UserORM = Depends(get_current_user)
) -> UserORM:
    if current_user.role == UserRole.ADMIN:
        return current_user

    if current_user.id != user_id:
        raise OnlyForOwnerError()
    return current_user

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
