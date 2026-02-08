import asyncio
import json

from pathlib import Path
from sqlalchemy import insert

from app.db.session import AsyncSessionLocal
from app.models.app_module import App_module

# JSON seed file
DATA_FILE = Path("scripts/seed/data/modules.json") 

async def create_modules():
    async with AsyncSessionLocal() as db:
        print("\n🌱 Bulk inserting MODULES...")
        data = json.loads(DATA_FILE.read_text())
        # Remove the "actions" key for module insert
        clean_data = [
            {k: v for k, v in item.items() if k != "actions"} 
            for item in data
        ]
        stmt = insert(App_module)
        await db.execute(stmt, clean_data)
        await db.commit()
        print("✅ Bulk inserting MODULES complete!")

if __name__ == "__main__":
    asyncio.run(create_modules())
