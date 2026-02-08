import asyncio
import json

from pathlib import Path
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_type import User_type
from app.models.user_type_access import User_type_access
from app.models.app_module_action import App_module_action

# JSON seed file
DATA_FILE = Path("scripts/seed/data/administrator_module_actions.json") 

async def create_user_type_admin(db: AsyncSession):
    print("\n🌱 Insert USER TYPE...")
    
    data = json.loads(DATA_FILE.read_text())
    
    name = "Administrator"
    
    # insert user type
    user_type = User_type(name=name, description="", is_editable=0)
    db.add(user_type)
    await db.flush()
    user_type_id = user_type.user_type_id
    
    # Prepare User_type_access records
    access_records = []
    for module in data:
        module_id = module["app_module_id"]
        action_ids = module.get("app_action_ids", [])

        for action_id in action_ids:
            # Get the app_module_action_id for this module + action pair
            result = await db.execute(
                select(App_module_action.app_module_action_id)
                .where(
                    App_module_action.app_module_id == module_id,
                    App_module_action.app_action_id == action_id
                )
            )
            row = result.scalar_one_or_none()
            if row:
                access_records.append({
                    "user_type_id"          : user_type_id,
                    "app_module_action_id"  : row,
                    "is_active"             : 1  # Active
                })
    
    # insert user type access here 
    if access_records:
        stmt = insert(User_type_access)
        await db.execute(stmt, access_records)
        await db.flush()
    
    print("✅ Insert USER TYPE complete!")
    return user_type_id

if __name__ == "__main__":
    asyncio.run(create_user_type_admin())
