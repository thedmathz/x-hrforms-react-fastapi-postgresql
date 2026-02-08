import asyncio
import json
from pathlib import Path

from app.db.session import AsyncSessionLocal
from app.models.app_action import App_action

# JSON seed file
DATA_FILE = Path("scripts/seed/data/actions.json") 

async def create_actions():
    async with AsyncSessionLocal() as db:

        print("\n🌱 Seeding Modules + Actions...\n")

        # Load JSON data
        modules_data = json.loads(DATA_FILE.read_text())

        print(modules_data)

    #     for module_item in modules_data:
    #         module_name = module_item["name"]
    #         actions_list = module_item["actions"]

    #         # -----------------------------
    #         # 1. Insert Module
    #         # -----------------------------
    #         module = db.query(AppModule).filter_by(name=module_name).first()

    #         if not module:
    #             module = AppModule(name=module_name)
    #             db.add(module)
    #             db.commit()
    #             db.refresh(module)
    #             print(f"✅ Module created: {module_name}")
    #         else:
    #             print(f"⚠️ Module exists: {module_name}")

    #         # -----------------------------
    #         # 2. Insert Actions + Pivot Links
    #         # -----------------------------
    #         for action_name in actions_list:

    #             # Insert Action if missing
    #             action = db.query(AppAction).filter_by(name=action_name).first()

    #             if not action:
    #                 action = AppAction(name=action_name)
    #                 db.add(action)
    #                 db.commit()
    #                 db.refresh(action)
    #                 print(f"   ➕ Action created: {action_name}")

    #             # Insert Pivot Mapping
    #             exists = (
    #                 db.query(AppModuleAction)
    #                 .filter_by(module_id=module.id, action_id=action.id)
    #                 .first()
    #             )

    #             if not exists:
    #                 mapping = AppModuleAction(
    #                     module_id=module.id,
    #                     action_id=action.id
    #                 )
    #                 db.add(mapping)
    #                 db.commit()
    #                 print(f"   🔗 Linked {module_name} → {action_name}")
    #             else:
    #                 print(f"   ⚠️ Already linked: {module_name} → {action_name}")

    #     db.close()
    #     print("\n🎉 Module + Action seeding complete!\n")


if __name__ == "__main__":
    asyncio.run(create_actions())
