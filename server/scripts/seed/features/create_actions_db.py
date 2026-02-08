import asyncio
import json

from pathlib import Path
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_action import App_action

# JSON seed file
DATA_FILE = Path("scripts/seed/data/actions.json") 

async def create_actions(db: AsyncSession):
    print("\n🌱 Bulk inserting ACTIONS...")
    data = json.loads(DATA_FILE.read_text())
    db.add_all([App_action(**a) for a in data])
    print("✅ Bulk inserting ACTIONS complete!")

if __name__ == "__main__":
    asyncio.run(create_actions())
