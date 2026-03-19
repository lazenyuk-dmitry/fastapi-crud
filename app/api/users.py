from fastapi import APIRouter, Depends
from app.schemas import User, UserCreate, UserUpdate, AppResult
from app.dependencies import UserServiceDep, admin_only, admin_or_owner

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User)
async def create_user(user_data: UserCreate, user_service: UserServiceDep):
    return await user_service.create(user_data)

@router.get("/", response_model=list[User], dependencies=[Depends(admin_only)])
async def get_users(user_service: UserServiceDep):
    return await user_service.get_all()

@router.get("/{user_id}", response_model=User, dependencies=[Depends(admin_or_owner)])
async def get_user(user_id: int, user_service: UserServiceDep):
    user = await user_service.get_one(user_id)
    return user

@router.put("/{user_id}", response_model=User, dependencies=[Depends(admin_or_owner)])
async def update_user(user_id: int, user_data: UserUpdate, user_service: UserServiceDep):
    user = await user_service.update(user_id, user_data)
    return user

@router.delete("/{user_id}", response_model=AppResult, dependencies=[Depends(admin_or_owner)])
async def delete_user(user_id: int, user_service: UserServiceDep):
    result = await user_service.delete(user_id)
    return AppResult(message = result)
