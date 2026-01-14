from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.starter_repository import StarterRepository
# from app.models.position import Position
# from app.schemas.position import PositionInsert, PositionUpdate
# from app.utils.fernet_util import fernet_encrypt, fernet_decrypt

from app.core.constants import APP_MODULES, APP_ACTIONS 

from app.utils.response_util import response_api

class StarterService:
    
    def __init__(self): self.repo = StarterRepository() 

    async def index(self, db: AsyncSession): 

        user_id     = 0

        username    = "admin"
        modules     = APP_MODULES
        actions     = APP_ACTIONS
        
        office_code = "HQ"
        office_name = "Headquarters"
        
        position_code = "IT1"
        position_name = "IT Associate 1"
        
        user_type = "Administrator"
        
        data = response_api(200)

        async with db.begin():
            
            has_admin = await self.repo.user_username_exist(db, username)
            
            # validation
            if has_admin:
                response_api(400, "Admin user already exists", "Invalid")
            
            # insert modules/actions/module-actions
            await self.repo.bulk_module_insert(db, modules)
            await self.repo.bulk_action_insert(db, actions)
            await self.repo.bulk_module_action_insert(db, modules)

            # insert office, position, user_type, user
            office_id = await self.repo.temp_new_office(db, office_code, office_name)
            position_id = await self.repo.temp_new_position(db, position_code, position_name)
            user_type_id = await self.repo.temp_new_user_type(db, user_type)
            user_id = await self.repo.temp_new_user(db, username, user_type_id, office_id, position_id)
            
            data['id'] = user_id

        return data

