from fastapi import FastAPI, HTTPException, Request
from app.database import engine
from app.api import users, auth
from app.exceptions import AppError
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(title="User Service API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    raise HTTPException(
        status_code=exc.status_code,
        detail = exc.detail
    )
