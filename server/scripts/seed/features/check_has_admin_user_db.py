import asyncio
import json

from pathlib import Path

from app.db.session import AsyncSessionLocal
from app.models.app_action import App_action

# JSON seed file
DATA_FILE = Path("scripts/seed/data/actions.json") 

async def check_has_admin_user():
    async with AsyncSessionLocal() as db:
        return False

if __name__ == "__main__":
    asyncio.run(check_has_admin_user())
