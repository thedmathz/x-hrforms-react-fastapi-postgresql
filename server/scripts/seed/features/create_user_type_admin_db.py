import asyncio
import json

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_type import User_type

async def create_user_type_admin(db: AsyncSession):
    print("\n🌱 Insert USER TYPE...")
    
    user_type = "Administrator"
    
    position = Position(code=position_code, name=position_name)
    db.add(position)
    await db.flush()
    
    print("✅ Insert USER TYPE complete!")
    return position.position_id

if __name__ == "__main__":
    asyncio.run(create_user_type_admin())
