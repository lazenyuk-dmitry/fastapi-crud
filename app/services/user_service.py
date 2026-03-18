from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import UserORM
from app.schemas import UserCreate

class UserService:
    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(select(UserORM))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate):
        new_user = UserORM(**user_data.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int):
        user = await db.get(UserORM, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False
