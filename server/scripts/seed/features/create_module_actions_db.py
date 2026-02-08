import asyncio
import json

from pathlib import Path
from sqlalchemy import insert

from app.db.session import AsyncSessionLocal
from app.models.app_module_action import App_module_action

# JSON seed file
DATA_FILE = Path("scripts/seed/data/modules.json") 

async def create_module_actions():
    async with AsyncSessionLocal() as db:
        print("\n🌱 Bulk inserting MODULE ACTIONS...")
        data = json.loads(DATA_FILE.read_text())
        # Prepare pivot table records
        pivot_records = []
        for module in data:
            module_id = module["app_module_id"]
            actions = module.get("actions", [])

            for action_id in actions:
                pivot_records.append({
                    "app_module_id": module_id,
                    "app_action_id": action_id
                })
        # Insert all pivot records in bulk
        if pivot_records:
            stmt = insert(App_module_action)
            await db.execute(stmt, pivot_records)
            await db.commit()
        print("✅ Bulk inserting MODULE ACTIONS complete!")

if __name__ == "__main__":
    asyncio.run(create_module_actions())
