import asyncio
import json

from pathlib import Path
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_module_action import App_module_action

# JSON seed file
DATA_FILE = Path("scripts/seed/data/modules.json") 

async def create_module_actions(db: AsyncSession):
    print("\n🌱 Bulk inserting MODULE ACTIONS...")
    data = json.loads(DATA_FILE.read_text())
    # bulk insert module-actions
    db.add_all([
            App_module_action(
                app_module_id=m["app_module_id"],
                app_action_id=action_id,
            )
            for m in data
            for action_id in m.get("actions", [])
        ])
    print("✅ Bulk inserting MODULE ACTIONS complete!")

if __name__ == "__main__":
    asyncio.run(create_module_actions())
