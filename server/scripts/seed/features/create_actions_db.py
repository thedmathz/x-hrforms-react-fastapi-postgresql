import asyncio
import json

from pathlib import Path
from sqlalchemy import insert

from app.db.session import AsyncSessionLocal
from app.models.app_action import App_action

# JSON seed file
DATA_FILE = Path("scripts/seed/data/actions.json") 

async def create_actions():
    async with AsyncSessionLocal() as db:
        print("\n🌱 Bulk inserting ACTIONS...")
        data = json.loads(DATA_FILE.read_text())
        stmt = insert(App_action)
        await db.execute(stmt, data)
        await db.commit()
        print("✅ Bulk inserting ACTIONS complete!")

if __name__ == "__main__":
    asyncio.run(create_actions())
