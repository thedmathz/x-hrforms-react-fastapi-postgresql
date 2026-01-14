from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.user_type import User_type
from app.models.token import Token

class RefreshTokenRepository:

    async def get_token_details(self, db: AsyncSession, token: str, user_id: int):
        result = await db.execute(
            select(
                Token.token_id, 
                Token.date_started, 
                Token.date_stopped, 
                Token.date_expiration, 
                Token.time_minute_used, 
                Token.time_minute_total, 
                Token.is_active, 
            )
            .where(Token.token == token)
            .where(Token.user_id == user_id)
        )
        return result.mappings().first()