from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from app.database import engine
from app.services.user_service import UserService
from app.schemas import User, UserCreate, UserUpdate, AuthUser
from typing import Annotated
from fastapi import Depends
from app.dependencies import get_user_service, admin_only, admin_or_owner
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import AuthHandler

app = FastAPI(title="User Service API")
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

@app.post("/users", response_model=User)
async def create_user(user_data: UserCreate, user_service: UserServiceDep):
    return await user_service.create(user_data)

@app.get("/users", response_model=list[User], dependencies=[Depends(admin_only)])
async def get_users(user_service: UserServiceDep):
    return await user_service.get_all()

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, user_service: UserServiceDep, _ = Depends(admin_or_owner)):
    user = await user_service.get_one(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, user_service: UserServiceDep, _ = Depends(admin_or_owner)):
    user = await user_service.update(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, user_service: UserServiceDep, _ = Depends(admin_or_owner)):
    success = await user_service.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.post("/login", response_model=AuthUser)
async def login(
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_service.get_by_email(form_data.username)

    if not user or not AuthHandler.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = AuthHandler.create_access_token(data={"sub": user.email, "role": user.role})
    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer",
    }
