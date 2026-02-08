import asyncio
import json

from pathlib import Path

from sqlalchemy import select

from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

# JSON seed file
DATA_FILE = Path("scripts/seed/data/actions.json") 

async def check_has_admin_user(db: AsyncSession):
    result = await db.execute(
        select(User)
        .where(User.username == "admin")
    )
    return result.scalar_one_or_none() is not None

if __name__ == "__main__":
    asyncio.run(check_has_admin_user())
