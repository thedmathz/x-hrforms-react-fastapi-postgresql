import random
import string

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse 
from app.repositories.user_repository import UserRepository
from app.utils.response_util import response_api 
from app.utils.fernet_util import fernet_encrypt, fernet_decrypt 
from app.utils.email_util import send_email, is_valid_email
from app.utils.argon2_util import argon2_encrypt 
from app.utils.common_util import smart_title
from app.core.config import settings

from app.schemas.user import UserInsert, UserUpdate 

class UserService:
    
    def __init__(self): self.repo = UserRepository() 

    async def index(self, db: AsyncSession): 
        
        data = response_api(200) 
        
        records = []
    
        temp_records = await self.repo.index(db) 
        for row in temp_records:
            records.append({
                "id"            : fernet_encrypt(str(row['user_id'])).decode(), 
                "user_type"     : row['user_type_name'], 
                "username"      : row['username'], 
                "firstname"     : row['first_name'], 
                "middlename"    : row['middle_name'], 
                "lastname"      : row['last_name'], 
                "office_code"   : row['office_code'],
                "position_code" : row['position_code'],
                "status"        : row['status'], 
            })
            
        data['records'] = records
        
        return JSONResponse(status_code=200, content=data)

    async def add(self, db: AsyncSession): 
        
        data = response_api(200) 
        
        user_types      = []
        offices         = []
        positions       = []
        recommenders    = []
        approvers       = []
        
        recommender_app_module_action_id    = await self.repo.get_module_action_id_by_name(db, 'For Approvals', 'Recommend')
        approver_app_module_action_id       = await self.repo.get_module_action_id_by_name(db, 'For Approvals', 'Approve')

        temp_user_types     = await self.repo.get_user_types(db)
        temp_offices        = await self.repo.get_offices(db)
        temp_positions      = await self.repo.get_positions(db)
        temp_recommenders   = await self.repo.get_recommenders(db, recommender_app_module_action_id)
        temp_approvers      = await self.repo.get_approvers(db, approver_app_module_action_id)

        if temp_user_types:
            for row in temp_user_types:
                user_types.append({
                    "id"    : row['user_type_id'],
                    "name"  : row['name'],
                })

        if temp_offices:
            for row in temp_offices:
                offices.append({
                    "id"    : row['office_id'],
                    "code"  : row['code'],
                    "name"  : row['name'],
                })

        if temp_positions:
            for row in temp_positions:
                positions.append({
                    "id"    : row['position_id'],
                    "code"  : row['code'],
                    "name"  : row['name'],
                })

        if temp_recommenders:
            for row in temp_recommenders:
                recommenders.append({
                    "id"        : row['user_id'],
                    "username"  : row['username'],
                    "name"      : f"{smart_title(row['last_name'])}, {smart_title(row['first_name'])} {smart_title(row['middle_name'])}",
                })

        if temp_approvers:
            for row in temp_approvers:
                approvers.append({
                    "id"        : row['user_id'], 
                    "username"  : row['username'], 
                    "name"      : f"{smart_title(row['last_name'])}, {smart_title(row['first_name'])} {smart_title(row['middle_name'])}",
                })

        data['user_types']      = user_types
        data['offices']         = offices
        data['positions']       = positions
        data['recommenders']    = recommenders
        data['approvers']       = approvers
        
        return JSONResponse(status_code=200, content=data)

    async def insert(self, db: AsyncSession, form_request: UserInsert): 
        
        data = response_api(200) 
        
        errors = ""
        
        '''
        Validation
        '''
        body_fields = {
            "user_type_id": {
                "label"     : "User Type", 
                "not_in"    : ["", 0, None], 
            }, 
            "username" : {
                "label"     : "Username", 
                "not_in"    : ["", None], 
            }, 
            "email" : {
                "label"     : "Email Address", 
                "not_in"    : ["", None], 
            }, 
            "office_id" : {
                "label"     : "Office", 
                "not_in"    : ["", 0, None], 
            }, 
            "position_id" : {
                "label"     : "Position", 
                "not_in"    : ["", 0, None], 
            }, 
            "recommender_id" : {
                "label"     : "Recommender", 
                "not_in"    : ["", 0, None], 
            }, 
            "approver_id" : {
                "label"     : "Approver", 
                "not_in"    : ["", 0, None], 
            }, 
        }
        for field, rules in body_fields.items():
            value = getattr(form_request, field)
            if 'not_in' in rules:
                if value in rules['not_in']:
                    errors += (", " if errors else "") + f"{rules['label']}"
                    
        if errors:
            response_api(400, f"{errors}", "Required Fields:") 
            
        # check for duplicate username 
        if not await self.repo.validate_username_unique(db, form_request.username):
            response_api(400, f"Username already exists", "Duplicate Record") 
            
        # check if email is valid format 
        if not is_valid_email(form_request.email):
            response_api(400, f"Invalid email address format", "Oops!")
        
        # check if recommender_id and approver_id exist in users table 
        recommender_app_module_action_id    = await self.repo.get_module_action_id_by_name(db, 'For Approvals', 'Recommend')
        approver_app_module_action_id       = await self.repo.get_module_action_id_by_name(db, 'For Approvals', 'Approve')
        
        print(recommender_app_module_action_id)
        print(approver_app_module_action_id)
        
        if not await self.repo.validate_recommender_approver_ids(db, int(form_request.recommender_id), int(recommender_app_module_action_id), int(form_request.approver_id), int(approver_app_module_action_id)):
            response_api(400, f"Recommender or Approver does not exist", "Invalid Record")
        
        # insert user 
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        user_id = await self.repo.insert(db, form_request, argon2_encrypt(password)) 
        
        data['id'] = fernet_encrypt(str(user_id)).decode() 
        
        # send email for email validation 
        await send_email(
            form_request.email, 
            "Welcome to HR Forms", 
            f"Continue with youe account registration by filling out the remaining details. {settings.FRONTEND_URL}/register?id={data['id']}", 
            True 
        )
        
        return JSONResponse(status_code=200, content=data)

    async def view(self, db: AsyncSession, id: int): 
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        row = await self.repo.view(db, row_id) 
        if row:

            recommender = f'{smart_title(row.recommender_last_name)}, {smart_title(row.recommender_first_name)} {smart_title(row.recommender_middle_name)}'
            approver    = f'{smart_title(row.approver_last_name)}, {smart_title(row.approver_first_name)} {smart_title(row.approver_middle_name)}'
            
            data['row'] = {
                'username'      : row.username,
                'user_type'     : row.user_type_name,
                'first_name'    : row.first_name,
                'middle_name'   : row.middle_name,
                'last_name'     : row.last_name,
                'gender'        : 'Male' if row.gender==1 else 'Female',
                'birth_date'    : row.birth_date.strftime("%B %d, %Y") if row.birth_date else "",
                'email'         : row.email,
                'recommender'   : recommender if row.recommender_id else "",
                'approver'      : approver if row.approver_id else "",
                'status'        : row.status,
            }
            
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)

    async def edit(self, db: AsyncSession, id: int): 
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        '''
        Initialize variables
        '''
        user_types      = [] 
        offices         = [] 
        positions       = [] 
        recommenders    = [] 
        approvers       = [] 
        
        '''
        Declare variable values
        '''
        recommender_app_module_action_id    = await self.repo.get_module_action_id_by_name(db, 'For Approvals', 'Recommend')
        approver_app_module_action_id       = await self.repo.get_module_action_id_by_name(db, 'For Approvals', 'Approve')

        temp_user_types     = await self.repo.get_user_types(db)
        temp_offices        = await self.repo.get_offices(db)
        temp_positions      = await self.repo.get_positions(db)
        temp_recommenders   = await self.repo.get_recommenders(db, recommender_app_module_action_id)
        temp_approvers      = await self.repo.get_approvers(db, approver_app_module_action_id)
        
        if temp_user_types:
            for row in temp_user_types:
                user_types.append({
                    "id"    : row['user_type_id'],
                    "name"  : row['name'],
                })

        if temp_offices:
            for row in temp_offices:
                offices.append({
                    "id"    : row['office_id'],
                    "code"  : row['code'],
                    "name"  : row['name'],
                })

        if temp_positions:
            for row in temp_positions:
                positions.append({
                    "id"    : row['position_id'],
                    "code"  : row['code'],
                    "name"  : row['name'],
                })

        if temp_recommenders:
            for row in temp_recommenders:
                recommenders.append({
                    "id"        : row['user_id'],
                    "username"  : row['username'],
                    "name"      : f"{smart_title(row['last_name'])}, {smart_title(row['first_name'])} {smart_title(row['middle_name'])}",
                })

        if temp_approvers:
            for row in temp_approvers:
                approvers.append({
                    "id"        : row['user_id'], 
                    "username"  : row['username'], 
                    "name"      : f"{smart_title(row['last_name'])}, {smart_title(row['first_name'])} {smart_title(row['middle_name'])}",
                })

        data['user_types']      = user_types
        data['offices']         = offices
        data['positions']       = positions
        data['recommenders']    = recommenders
        data['approvers']       = approvers
        
        '''
        Get user data
        '''
        row = await self.repo.view(db, row_id) 
        if row:
            data['row'] = {
                'username'          : row.username,
                'user_type'         : row.user_type_name,
                'first_name'        : row.first_name,
                'middle_name'       : row.middle_name,
                'last_name'         : row.last_name,
                'gender'            : row.gender,
                'birth_date'        : row.birth_date if row.birth_date else "",
                'email'             : row.email,
                'recommender_id'    : row.recommender_id,
                'approver_id'       : row.approver_id,
                'status'            : row.status,
            }
            
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)

    async def update(self, db: AsyncSession, id: int, form_request: UserUpdate): 
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        errors = ""
        
        # check if user is admin username
        if await self.repo.is_admin_username(db, row_id):
            response_api(400, f"Cannot update admin user", "Action Not Allowed")
            
        # check if user status is pending
        if not await self.repo.is_user_pending(db, row_id):
            response_api(400, f"Only pending users can be updated", "Action Not Allowed") 
            
        is_pending_account = await self.repo.is_user_pending(db, row_id)
            
        '''
        Validation
        '''
        body_fields = {
            "user_type_id": {
                "label"     : "User Type", 
                "not_in"    : ["", 0, None], 
            }, 
            "email" : {
                "label"     : "Email Address", 
                "not_in"    : ["", None], 
            }, 
            "office_id" : {
                "label"     : "Office", 
                "not_in"    : ["", 0, None], 
            }, 
            "position_id" : {
                "label"     : "Position", 
                "not_in"    : ["", 0, None], 
            }, 
            "recommender_id" : {
                "label"     : "Recommender", 
                "not_in"    : ["", 0, None], 
            }, 
            "approver_id" : {
                "label"     : "Approver", 
                "not_in"    : ["", 0, None], 
            }, 
        }
        if not is_pending_account:
            body_fields['username'] = {
                "label"     : "Username", 
                "not_in"    : ["", None], 
            }
            
        for field, rules in body_fields.items():
            value = getattr(form_request, field)
            if 'not_in' in rules:
                if value in rules['not_in']:
                    errors += (", " if errors else "") + f"{rules['label']}"
                    
        if errors:
            response_api(400, f"{errors}", "Required Fields:") 
            
        # get existing record
        obj = await self.repo._record_does_exist(db, row_id)
        if not obj:
            response_api(400, "Record not found", "Invalid")
            
        # set changes
        obj.user_type_id     = form_request.user_type_id
        obj.username         = form_request.username
        obj.email            = form_request.email
        obj.office_id        = form_request.office_id
        obj.position_id      = form_request.position_id
        obj.recommender_id   = form_request.recommender_id
        obj.approver_id      = form_request.approver_id
        
        if not is_pending_account: 
            obj.username = form_request.username
            
        # update record
        await self.repo.update(db, obj)
        
        # if updated and past status is pending, send email for email validation with updated temporary password
        if is_pending_account:
            
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            # send email for email validation
            await send_email(
                form_request.email, 
                "Welcome to HR Forms", 
                f"Your temporary password has been updated and is: {password}. Log in and change your account details immediately in {settings.FRONTEND_URL}", 
                True 
            )
            
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)

    async def activate(self, db: AsyncSession, id: int):
         
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        # check if user status is pending
        if await self.repo.is_user_pending(db, row_id):
            response_api(400, f"Cannot activate pending user", "Action Not Allowed")
        
        # check if user is admin username
        if await self.repo.is_admin_username(db, row_id):
            response_api(400, f"Cannot update admin user", "Action Not Allowed")
            
        await self.repo.update_status(db, row_id, 1) 
        
        return JSONResponse(status_code=200, content=data)

    async def deactivate(self, db: AsyncSession, id: int): 
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        # check if user status is pending
        if await self.repo.is_user_pending(db, row_id):
            response_api(400, f"Cannot deactivate pending user", "Action Not Allowed")
        
        # check if user is admin username
        if await self.repo.is_admin_username(db, row_id):
            response_api(400, f"Cannot update admin user", "Action Not Allowed")
        
        await self.repo.update_status(db, row_id, -1) 
        
        return JSONResponse(status_code=200, content=data)
