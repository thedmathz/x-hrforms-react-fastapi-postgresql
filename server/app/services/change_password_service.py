from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse 
from app.repositories.change_password_repository import ChangePasswordRepository
from app.models.user import User
from app.schemas.change_password import ChangePasswordForm
from app.utils.response_util import response_api
from app.utils.argon2_util import argon2_encrypt, argon2_verify
from app.utils.common_util import is_strong_password

class ChangePasswordService:
    
    def __init__(self): self.repo = ChangePasswordRepository()

    async def index(self, db: AsyncSession, form_request: ChangePasswordForm, current_user_id: str):
        
        data = response_api(200) 
        
        errors = ""
        
        '''
        Validation
        '''
        body_fields = {
            "password_current": {
                "label"     : "Current Password",
                "not_in"    : ["", None],
            }, 
            "password_new": {
                "label"     : "New Password",
                "not_in"    : ["", None],
            }, 
            "password_confirm": {
                "label"     : "Confirm Password",
                "not_in"    : ["", None],
            }, 
        }
        for field, rules in body_fields.items():
            value = getattr(form_request, field)
            if 'not_in' in rules:
                if value in rules['not_in']:
                    errors += (", " if errors else "") + f"{rules['label']}"
                    
        if errors:
            response_api(400, f"{errors}", "Required Fields:")
            
        # invalid current password
        user = await self.repo.get_user_by_id(db, int(current_user_id))
        print(user.password)
        if not user or not argon2_verify(user.password, form_request.password_current):
            response_api(400, "Current password is incorrect", "Invalid")
        
        # new password is the same as current password
        if form_request.password_current == form_request.password_new:
            response_api(400, "New password cannot be the same as current password", "Invalid")
        
        # new password does not match confirm password
        if form_request.password_new != form_request.password_confirm:
            response_api(400, "New password and confirm password do not match", "Invalid")
        
        # password requirement 
        if not is_strong_password(form_request.password_new):
            response_api(400, "Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character.", "Weak Password")
        
        # change password
        await self.repo.index(db, int(current_user_id), argon2_encrypt(form_request.password_new)) 
        
        return JSONResponse(status_code=200, content=data)
