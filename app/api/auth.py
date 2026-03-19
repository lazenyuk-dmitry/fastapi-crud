from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import AuthUser
from app.dependencies import UserServiceDep
from app.auth import AuthHandler
from app.exceptions import IncorrectEmailOrPasswordError

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=AuthUser)
async def login(
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_service.get_by_email(form_data.username)

    if not user or not AuthHandler.verify_password(form_data.password, user.hashed_password):
        raise IncorrectEmailOrPasswordError()

    access_token = AuthHandler.create_access_token(data={"sub": user.email, "role": user.role})
    return AuthUser(
        user = user,
        access_token = access_token,
        token_type = "bearer",
    )
