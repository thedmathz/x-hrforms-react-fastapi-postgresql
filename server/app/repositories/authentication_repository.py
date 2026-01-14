from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.user_type import User_type
from app.models.token import Token

class AuthenticationRepository:

    async def get_user_by_username(self, db: AsyncSession, username: str):
        result = await db.execute(
            select(
                User.user_id, 
                User.password, 
                User.status, 
            ).where(User.username == username).where(User.status != 0) 
        )
        return result.mappings().first()

    async def get_user_by_user_id(self, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(
                User.username,
                User_type.name.label("user_type_name"), 
            )
            .join(User_type, User.user_type_id == User_type.user_type_id, isouter=True) 
            .where(User.user_id == user_id)
            .where(User.status == 1)
        )
        return result.mappings().first()

    async def insert_new_token(self, db: AsyncSession, obj: Token):
        db.add(obj)
        return await db.flush() 

    async def get_token_by_value(self, db: AsyncSession, token: str):
        result = await db.execute(
            select(Token)
            .where(Token.token == token)
            .where(Token.is_active == 1)
        )
        return result.scalars().first()