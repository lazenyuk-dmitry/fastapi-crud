from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import UserORM
from app.schemas import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(UserORM))
        return result.scalars().all()

    async def create(self, user_data: UserCreate):
        new_user = UserORM(**user_data.model_dump())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_one(self, user_id: int):
        result = await self.db.execute(select(UserORM).where(UserORM.id == user_id))
        return result.scalar_one_or_none()

    async def update(self, user_id: int, user_data: UserUpdate):
        user = await self.get_one(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int):
        user = await self.get_one(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False
