import datetime 
import random 
import os 
import shutil 

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse 
from PIL import Image
from app.repositories.my_profile_repository import MyProfileRepository
from app.utils.common_util import smart_title
from app.utils.response_util import response_api 
from app.utils.email_util import send_email, is_valid_email
from app.schemas.my_profile import MyProfileUpdate, MyProfileEmailOtp, MyProfileEmailUpdate 
from app.core.config import settings 

class MyProfileService:
    
    def __init__(self): self.repo = MyProfileRepository()

    async def index(self, request: Request, db: AsyncSession, current_user_id: int):
        
        data = response_api(200) 
        
        base_url = str(request.base_url).rstrip("/")
        
        avatar = "/assets/images/default.jpg"
        
        # get user profile data logic goes here 
        row = await self.repo.index(db, current_user_id) 
        if row:
            data['row'] = {
                'avatar'        : f'{base_url}{avatar}',
                'username'      : row.username,
                'first_name'    : smart_title(row.first_name),
                'middle_name'   : smart_title(row.middle_name),
                'last_name'     : smart_title(row.last_name),
                'gender'        : 'Male' if row.gender == 1 else 'Female',
                'birth_date'    : datetime.datetime.strftime(row.birth_date, '%B %d, %Y') if row.birth_date else None,
            }
            
        return JSONResponse(status_code=200, content=data)

    async def edit(self, request: Request, db: AsyncSession, current_user_id: int):
        
        data = response_api(200) 
        
        base_url = str(request.base_url).rstrip("/")
        
        avatar = "/assets/images/default.jpg"
        
        # get user profile data logic goes here 
        row = await self.repo.edit(db, current_user_id) 
        if row:
            data['row'] = {
                'avatar'        : f'{base_url}{avatar}',
                'username'      : row.username,
                'first_name'    : smart_title(row.first_name),
                'middle_name'   : smart_title(row.middle_name),
                'last_name'     : smart_title(row.last_name),
                'gender'        : row.gender,
                'birth_date'    : datetime.datetime.strftime(row.birth_date, '%Y-%m-%d') if row.birth_date else None,
            }
            
        return JSONResponse(status_code=200, content=data)

    async def update(self, db: AsyncSession, form_request: MyProfileUpdate, current_user_id: int):
        
        data = response_api(200) 
        
        errors = ""
        
        '''
        Validation
        '''
        body_fields = {
            "first_name": {
                "label"     : "First Name",
                "not_in"    : ["", None],
            }, 
            "last_name": {
                "label"     : "Last Name",
                "not_in"    : ["", None],
            }, 
            "gender": {
                "label"     : "Gender",
                "not_in"    : ["", None],
            }, 
            "birth_date": {
                "label"     : "Birth Date",
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
        
        # update user basic profile data logic goes here 
        obj = await self.repo.get_user_details(db, current_user_id)
        if not obj:
            response_api(400, "Record not found", "Invalid")
            
        # Apply changes in API or in service
        for field, value in form_request.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        
        await self.repo.update(db, obj)
        
        return JSONResponse(status_code=200, content=data)

    async def edit_email(self, db: AsyncSession, current_user_id: int):
        
        data = response_api(200) 
        
        # get user profile data logic goes here 
        row = await self.repo.edit_email(db, current_user_id) 
        if row:
            data['row'] = { 'email' : row.email }
            
        return JSONResponse(status_code=200, content=data)

    async def set_email_otp(self, db: AsyncSession, form_request: MyProfileEmailOtp, current_user_id: int):
        
        data = response_api(200) 
        
        email_otp = random.randint(100000, 999999)
        email_otp_valid_until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.EMAIL_OTP_EXPIRY_MINUTES)
        
        # check if email format is valid 
        if not is_valid_email(form_request.email): 
            response_api(400, "Invalid email format", "Oops!") 
        
        # get user details 
        obj = await self.repo.get_user_details(db, current_user_id) 
        if not obj: 
            response_api(400, "Record not found", "Invalid") 
        
        # update user email, otp, and validity period 
        obj.email_otp = str(email_otp)
        obj.email_otp_valid_until = email_otp_valid_until
        
        await self.repo.update(db, obj)
        
        # send email 
        formatted = (
            datetime.datetime.fromisoformat(str(email_otp_valid_until))
            .astimezone(datetime.timezone(datetime.timedelta(hours=8)))
            .strftime("%m/%d/%Y %I:%M %p")
        )
        email_message = f'<b>{str(email_otp)}</b> is your account OTP valid until {formatted}.'
        
        await send_email(form_request.email, "Account OTP", email_message, True)
            
        return JSONResponse(status_code=200, content=data)

    async def update_email(self, db: AsyncSession, form_request: MyProfileEmailUpdate, current_user_id: int): 
        
        data = response_api(200) 
        
        # get user details 
        obj = await self.repo.get_user_details(db, current_user_id) 
        if not obj: 
            response_api(400, "Record not found", "Invalid") 
            
        if form_request.email_otp != obj.email_otp:
            response_api(400, "Invalid OTP", "Oops!") 
            
        # update user email, otp, and validity period 
        for field, value in form_request.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        obj.date_email_validated = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.EMAIL_OTP_EXPIRY_MINUTES)
        
        await self.repo.update(db, obj)
        
        return JSONResponse(status_code=200, content=data)
    
    async def update_avatar(self, db: AsyncSession, current_user_id: int, file):
        
        data = response_api(200) 
        
        UPLOAD_DIR = "media/uploads/user_profile_pictures" 
        
        # Ensure upload dir exists
        user_dir = os.path.join(UPLOAD_DIR, current_user_id)
        if os.path.exists(user_dir):
            # Clear contents
            for filename in os.listdir(user_dir):
                file_path = os.path.join(user_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # delete file or link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # delete folder and its contents
        else:
            # Create directory if it doesn't exist
            os.makedirs(user_dir)

        # Generate a unique filename
        file_ext = file.filename.split(".")[-1]
        filename = f"default.{file_ext}"
        file_path = os.path.join(user_dir, filename)

        # Save original
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Open image and create resized versions
        sizes = {
            "thumbnail": (150, 150),        # small previews, icons
            "small": (300, 300),            # in-content images on mobile
            "medium": (768, 768),           # medium layout images, responsive
            "medium_large": (1024, 1024),   # larger responsive images
            "large": (2048, 2048),          # high-res/full-screen images
        }
        for size_name, dimensions in sizes.items():
            img = Image.open(file_path)
            img.thumbnail(dimensions)
            resized_path = os.path.join(user_dir, f"{size_name}.{file_ext}")
            img.save(resized_path)
        
        return JSONResponse(status_code=200, content=data)
