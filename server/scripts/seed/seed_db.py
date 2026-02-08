import asyncio

from app.db.session import AsyncSessionLocal

from scripts.seed.features.check_has_admin_user_db import check_has_admin_user 
from scripts.seed.features.create_actions_db import create_actions 
from scripts.seed.features.create_modules_db import create_modules 
from scripts.seed.features.create_module_actions_db import create_module_actions 
from scripts.seed.features.create_office_db import create_office 
from scripts.seed.features.create_position_db import create_position 
from scripts.seed.features.create_user_type_admin_db import create_user_type_admin 
from scripts.seed.features.create_user_admin_db import create_user_admin 

async def init():
    
    print("\n🚀 Initializing Database...\n")
    async with AsyncSessionLocal() as db:
        async with db.begin():
            if not await check_has_admin_user(db):
                await create_modules(db)
                await create_actions(db)
                await create_module_actions(db)
                office_id = await create_office(db)
                position_id = await create_position(db)
                user_type_id = await create_user_type_admin(db)
                # await create_user_admin(db)
    print("\n🎉 Database fully initialized!\n")

if __name__ == "__main__":
    asyncio.run(init())
