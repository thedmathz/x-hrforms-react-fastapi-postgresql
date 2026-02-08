import asyncio

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
    if not await check_has_admin_user():
        await create_actions()
        # await create_modules()
        # await create_module_actions()
        # await create_office()
        # await create_position()
        # await create_user_type_admin()
        # await create_user_admin()
    print("\n🎉 Database fully initialized!\n")

if __name__ == "__main__":
    asyncio.run(init())
