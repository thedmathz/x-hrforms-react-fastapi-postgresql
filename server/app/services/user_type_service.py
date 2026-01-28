from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse 
from app.repositories.user_type_repository import UserTypeRepository
from app.schemas.user_type import UserTypeInsert, UserTypeUpdate
from app.utils.response_util import response_api 
from app.utils.fernet_util import fernet_encrypt, fernet_decrypt 
from app.models.user_type_access import User_type_access

class UserTypeService:
    
    def __init__(self): self.repo = UserTypeRepository()

    async def index(self, db: AsyncSession): 
        
        data = response_api(200) 
        
        records = []
    
        temp_records = await self.repo.index(db) 
        for row in temp_records:
            records.append({
                "id": fernet_encrypt(str(row.user_type_id)).decode(), 
                "name": row.name, 
                "description": row.description, 
            })
            
        data['records'] = records
        
        return JSONResponse(status_code=200, content=data)

    async def add(self, db: AsyncSession):
        
        data = response_api(200) 
        
        module_actions = []
        
        # get app modules 
        temp_modules = await self.repo.get_app_modules(db)
        for row in temp_modules:
            
            temp_actions = await self.repo.get_app_actions_by_module_id(db, row.app_module_id)
            
            actions = []
            for action_row in temp_actions:
                actions.append({
                    "app_module_action_id" : action_row['app_module_action_id'], 
                    "action" : action_row['name'], 
                })
            
            module_actions.append({
                "module" : row.name, 
                "actions" : actions,
            }) 
        
        data['module_actions'] = module_actions 
        
        return JSONResponse(status_code=200, content=data)

    async def insert(self, db: AsyncSession, form_request: UserTypeInsert):
        
        data = response_api(200) 
        
        errors = ""
        
        '''
        Validation
        '''
        body_fields = {
            "name": {
                "label"     : "User Type Name",
                "not_in"    : ["", None],
            }, 
            "app_module_action_ids" : {
                "label"     : "Access Rights",
                "not_in"    : [[], "", None],
            }, 
        }
        for field, rules in body_fields.items():
            value = getattr(form_request, field)
            if 'not_in' in rules:
                if value in rules['not_in']:
                    errors += (", " if errors else "") + f"{rules['label']}"
                    
        if errors:
            response_api(400, f"{errors}", "Required Fields:") 
            
        # duplicate name check can be added here 
        if not await self.repo.validate_user_type_name_unique(db, form_request.name):
            response_api(400, f"User Type Name already exists", "Duplicate Record") 
            
        # all access rights inputted must be in database to prevent tampering 
        if not await self.repo.validate_app_module_action_ids(db, form_request.app_module_action_ids):
            response_api(400, f"Invalid Access Rights", "Oops!")
        
        user_type_id = await self.repo.insert(db, form_request.name, form_request.description)
        await self.repo.bulk_user_type_access_insert(db, user_type_id, form_request.app_module_action_ids)
            
        data['id'] = user_type_id
        
        return JSONResponse(status_code=200, content=data)

    async def view(self, db: AsyncSession, id: str):
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        # get user type details
        row = await self.repo.view(db, row_id) 
        if row:
            access_rights = [] 
            
            temp_access_rights = await self.repo.get_user_type_access_rights(db, row_id) 
            if temp_access_rights:
                for ar in temp_access_rights:
                    access_rights.append(ar['app_module_action_id'])
            
            data['row'] = {
                'name'          : row.name,
                'description'   : row.description,
                'access_rights' : access_rights,
            }
        
            # get app modules 
            module_actions = []

            temp_modules = await self.repo.get_app_modules(db)
            for tm in temp_modules:
                
                temp_actions = await self.repo.get_app_actions_by_module_id(db, tm.app_module_id)
                
                actions = []
                for action_row in temp_actions:
                    actions.append({
                        "app_module_action_id" : action_row['app_module_action_id'], 
                        "action" : action_row['name'], 
                    })
                
                module_actions.append({
                    "module" : tm.name, 
                    "actions" : actions,
                }) 
                
            data['module_actions'] = module_actions
            
        data['id'] = id 
            
        return JSONResponse(status_code=200, content=data)

    async def edit(self, db: AsyncSession, id: str):
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        obj = await self.repo._record_does_exist(db, row_id)
        if not obj:
            response_api(400, "Record not found", "Invalid")
            
        # cant be edited if is_editable is 0
        if obj.is_editable == 0:
            response_api(400, "This user type cannot be edited", "Invalid") 
        
        # get user type details
        row = await self.repo.view(db, row_id) 
        if row:
            access_rights = [] 
            
            temp_access_rights = await self.repo.get_user_type_access_rights(db, row_id) 
            if temp_access_rights:
                for ar in temp_access_rights:
                    access_rights.append(ar['app_module_action_id'])
            
            data['row'] = {
                'name'          : row.name,
                'description'   : row.description,
                'access_rights' : access_rights,
            }
        
            # get app modules 
            module_actions = []
            
            temp_modules = await self.repo.get_app_modules(db)
            for tm in temp_modules:
                
                temp_actions = await self.repo.get_app_actions_by_module_id(db, tm.app_module_id)
                
                actions = []
                for action_row in temp_actions:
                    actions.append({
                        "app_module_action_id" : action_row['app_module_action_id'], 
                        "action" : action_row['name'], 
                    })
                
                module_actions.append({
                    "module" : tm.name, 
                    "actions" : actions,
                }) 
                
            data['module_actions'] = module_actions
            
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)

    async def update(self, db: AsyncSession, id: str, form_request: UserTypeUpdate):
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        # check if record exists
        obj = await self.repo._record_does_exist(db, row_id)
        if not obj:
            response_api(400, "Record not found", "Invalid")
            
        # cant be edited if is_editable is 0
        if obj.is_editable == 0:
            response_api(400, "This user type cannot be edited", "Invalid") 
        
        errors = ""
        
        '''
        Validation
        '''
        body_fields = {
            "name": {
                "label"     : "User Type Name",
                "not_in"    : ["", None],
            }, 
            "app_module_action_ids" : {
                "label"     : "Access Rights",
                "not_in"    : [[], "", None],
            }, 
        }
        for field, rules in body_fields.items():
            value = getattr(form_request, field)
            if 'not_in' in rules:
                if value in rules['not_in']:
                    errors += (", " if errors else "") + f"{rules['label']}"
                    
        if errors:
            response_api(400, f"{errors}", "Required Fields:") 
            
        # duplicate name check can be added here 
        if not await self.repo.validate_user_type_name_unique(db, form_request.name, row_id):
            response_api(400, f"User Type Name already exists", "Duplicate Record") 
        
        # all access rights inputted must be in database to prevent tampering 
        if not await self.repo.validate_app_module_action_ids(db, form_request.app_module_action_ids):
            response_api(400, f"Invalid Access Rights", "Oops!")
            
        # update user type access first
        obj.name = form_request.name
        obj.description = form_request.description
        user_type_id = await self.repo.update(db, obj)
        
        # deactivate all existing access rights
        await self.repo.bulk_user_type_access_deactivate(db, user_type_id) 
        
        # insert or update access rights
        for app_module_action_id in form_request.app_module_action_ids:
            does_exist = await self.repo.user_type_access_record_does_exist(db, user_type_id, app_module_action_id)
            if does_exist:
                # reactivate
                does_exist.is_active = 1
                await self.repo.save_user_type_access(db, does_exist)
            else:
                # insert new record
                await self.repo.save_user_type_access(db, 
                    User_type_access(
                        user_type_id = user_type_id, 
                        app_module_action_id = app_module_action_id, 
                        is_active = 1, 
                    )
                )
            
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)

    async def delete(self, db: AsyncSession, id: str):
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        obj = await self.repo._record_does_exist(db, row_id)
        if not obj:
            response_api(400, "Record not found", "Invalid")
            
        # cant be deleted if is_editable is 0
        if obj.is_editable == 0:
            response_api(400, "This user type cannot be deleted", "Invalid") 
        
        # delete user type access first
        await self.repo.bulk_user_type_access_delete(db, row_id)
        
        # delete user type
        await self.repo.delete(db, obj)
        
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)
