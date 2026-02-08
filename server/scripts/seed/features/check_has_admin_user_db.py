import asyncio
import json

from pathlib import Path

from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.user import User

# JSON seed file
DATA_FILE = Path("scripts/seed/data/actions.json") 

async def check_has_admin_user():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User)
            .where(User.username == "admin")
        )
        return result.scalar_one_or_none() is not None

if __name__ == "__main__":
    asyncio.run(check_has_admin_user())
