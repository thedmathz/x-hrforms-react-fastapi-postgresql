from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.user import User
from app.models.user_type import User_type

class ForgotPasswordRepository:

    async def get_user_by_username(self, db: AsyncSession, username: str):
        stmt = (
            select(User)
            .where(User.username == username)
            .where(User.status == 1)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_user_id(self, db: AsyncSession, user_id: int):
        stmt = (
            select(User)
            .where(User.user_id == user_id)
            .where(User.status == 1)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update_user(self, db: AsyncSession, obj: User): 
        await db.commit()
        await db.refresh(obj) 
        
    async def reset_password(self, db: AsyncSession, user_id: int, new_password: str): 
        await db.execute(
            update(User)
            .where(User.user_id == user_id)
            .values(password=new_password)
        )
        await db.commit()
