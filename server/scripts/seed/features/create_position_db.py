import asyncio
import json

from pathlib import Path
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.position import Position

async def create_position(db: AsyncSession):
    print("\n🌱 Insert POSITION...")
    
    position_code = "IT1"
    position_name = "IT ASSOCIATE 1"
    
    position = Position(code=position_code, name=position_name)
    db.add(position)
    await db.flush()
    
    print("✅ Insert POSITION complete!")
    return position.position_id

if __name__ == "__main__":
    asyncio.run(create_position())
