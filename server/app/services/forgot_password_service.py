import datetime 
import random 
import os 
import shutil 

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse 
from PIL import Image
from app.repositories.forgot_password_repository import ForgotPasswordRepository
from app.utils.response_util import response_api 
from app.utils.fernet_util import fernet_encrypt, fernet_decrypt
from app.schemas.forgot_password import ForgotPasswordUsername, ForgotPasswordOtp, ForgotPasswordReset
from app.utils.email_util import send_email, is_valid_email
from app.core.config import settings 
from app.utils.common_util import is_strong_password 
from app.utils.argon2_util import argon2_encrypt

class ForgotPasswordService:
    
    def __init__(self): self.repo = ForgotPasswordRepository()

    async def check_username(self, db: AsyncSession, form_request: ForgotPasswordUsername):
        
        data = response_api(200) 
        
        # get active user by username 
        obj = await self.repo.get_user_by_username(db, form_request.username) 
        if not obj: 
            response_api(400, "Unknown account", "Invalid") 
            
        # check if it has email 
        if not is_valid_email(obj.email): 
            response_api(400, "Account has no valid email address", "Oops") 
        
        # send email message 
        forgot_password_otp = random.randint(100000, 999999) 
        email_message = f'<b>{forgot_password_otp}</b> is your forgot password OTP.' 
        await send_email(obj.email, "Forgot Password OTP", email_message, True) 
        
        # update otp in database 
        obj.forgot_password_otp = str(forgot_password_otp) 
        obj.forgot_password_otp_valid_until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.EMAIL_OTP_EXPIRY_MINUTES) 
        await self.repo.update_user(db, obj) 
        
        data['code'] = fernet_encrypt(str(obj.user_id)).decode() 
        
        return JSONResponse(status_code=200, content=data) 

    async def resend_otp(self, db: AsyncSession, code: str):
        
        user_id = int(fernet_decrypt(code)) 
        
        data = response_api(200) 
        
        # get active user by username 
        obj = await self.repo.get_user_by_user_id(db, user_id) 
        if not obj:
            response_api(400, "Unknown account", "Invalid") 
        
        # check if it has email 
        if not is_valid_email(obj.email):
            response_api(400, "Account has no valid email address", "Oops")
        
        # send email message 
        forgot_password_otp = random.randint(100000, 999999)
        email_message = f'<b>{forgot_password_otp}</b> is your new forgot password OTP.'
        await send_email(obj.email, "New Forgot Password OTP", email_message, True)
        
        # update otp in database 
        obj.forgot_password_otp = str(forgot_password_otp)
        obj.forgot_password_otp_valid_until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.EMAIL_OTP_EXPIRY_MINUTES)
        await self.repo.update_user(db, obj) 
        
        return JSONResponse(status_code=200, content=data)

    async def otp(self, db: AsyncSession, code: str):
        
        user_id = int(fernet_decrypt(code)) 
        
        data = response_api(200) 
        
        # get active user by username 
        obj = await self.repo.get_user_by_user_id(db, user_id) 
        if not obj:
            response_api(400, "Unknown account", "Invalid") 
            
        data['username'] = obj.username
        data['email'] = obj.email
        
        return JSONResponse(status_code=200, content=data)

    async def check_otp(self, db: AsyncSession, code: str, form_request: ForgotPasswordOtp):
        
        user_id = int(fernet_decrypt(code)) 
        
        data = response_api(200) 
        
        # get active user by username 
        obj = await self.repo.get_user_by_user_id(db, user_id) 
        if not obj:
            response_api(400, "Unknown account", "Invalid") 
        
        # check otp
        forgot_password_otp = form_request.forgot_password_otp
        
        # empty otp
        if not forgot_password_otp:
            response_api(400, "Please enter OTP", "Invalid")
        
        # invalid otp 
        if obj.forgot_password_otp != forgot_password_otp:
            response_api(400, "Invalid OTP", "Oops")
        
        # expired otp 
        if obj.forgot_password_otp_valid_until < datetime.datetime.now(datetime.timezone.utc):
            response_api(400, "OTP has expired", "Oops")
        
        return JSONResponse(status_code=200, content=data)

    async def reset_password(self, db: AsyncSession, code: str):
        
        user_id = int(fernet_decrypt(code)) 
        
        data = response_api(200) 
        
        # get active user by username 
        obj = await self.repo.get_user_by_user_id(db, user_id) 
        if not obj:
            response_api(400, "Unknown account", "Invalid") 
        
        data['username'] = obj.username
        
        return JSONResponse(status_code=200, content=data)

    async def check_reset_password(self, db: AsyncSession, code: str, form_request: ForgotPasswordReset):
        
        user_id = int(fernet_decrypt(code)) 
        
        data = response_api(200) 
        
        # get active user by username 
        obj = await self.repo.get_user_by_user_id(db, user_id) 
        if not obj:
            response_api(400, "Unknown account", "Invalid") 
        
        # fill all required fields
        if form_request.password_new == "" or form_request.password_confirm == "":
            response_api(400, "Please fill out all required fields", "Oops") 
        
        # new password does not match confirm password
        if form_request.password_new != form_request.password_confirm:
            response_api(400, "New password and confirm password do not match", "Invalid")
            
        # password requirement 
        if not is_strong_password(form_request.password_new):
            response_api(400, "Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character.", "Weak Password")
            
        # reset password
        await self.repo.reset_password(db, int(obj.user_id), argon2_encrypt(form_request.password_new))
            
        return JSONResponse(status_code=200, content=data)
    