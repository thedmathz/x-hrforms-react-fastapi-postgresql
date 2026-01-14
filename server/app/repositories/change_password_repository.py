from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.models.user import User

class ChangePasswordRepository:

    async def get_user_by_id(self, db: AsyncSession, user_id: int): 
        return await db.get(User, user_id)  

    async def index(self, db: AsyncSession, user_id: int, password: str): 
        await db.execute(
            update(User)
            .where(User.user_id == user_id)
            .values(password=password)
        )
        await db.commit()
