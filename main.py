from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base, get_db
from app.services.user_service import UserService
from app.schemas import User, UserCreate

app = FastAPI(title="User Service API")
user_service = UserService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

@app.post("/users", response_model=User)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.create(db, user_data)

@app.get("/users", response_model=list[User])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await UserService.get_all(db)
