import asyncio
import json

from pathlib import Path
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_module import App_module

# JSON seed file
DATA_FILE = Path("scripts/seed/data/modules.json") 

async def create_modules(db: AsyncSession):
    print("\n🌱 Bulk inserting MODULES...")
    # Load JSON data and prepare for bulk insert
    data = json.loads(DATA_FILE.read_text())
    # bulk insert modules
    db.add_all([
        App_module(
            app_module_id=m["app_module_id"],
            name=m["name"],
            rank=m["rank"]
        )
        for m in data
    ])
    print("✅ Bulk inserting MODULES complete!")

if __name__ == "__main__":
    asyncio.run(create_modules())
