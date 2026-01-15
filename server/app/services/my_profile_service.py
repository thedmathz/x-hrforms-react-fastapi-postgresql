import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse 
from app.repositories.my_profile_repository import MyProfileRepository
from app.models.user import User
from app.schemas.office import OfficeInsert, OfficeUpdate
from app.utils.fernet_util import fernet_encrypt, fernet_decrypt
from app.utils.response_util import response_api

class MyProfileService:
    
    def __init__(self): self.repo = MyProfileRepository()

    async def index(self, db: AsyncSession, user_id: int):
        
        data = response_api(200) 
        
        # get user profile data logic goes here 
        row = await self.repo.index(db, user_id) 
        if row:
            data['row'] = {
                'username'      : row.username,
                'first_name'    : row.first_name,
                'middle_name'   : row.middle_name,
                'last_name'     : row.last_name,
                'gender'        : row.gender,
                'birth_date'    : datetime.datetime.strftime(row.birth_date, '%B %d, %Y') if row.birth_date else None,
            }
            
        return JSONResponse(status_code=200, content=data)

    # async def edit(self, db: AsyncSession):
        
    #     data = response_api(200) 
        
    #     # get user profile data for editing logic goes here 
        
    #     return JSONResponse(status_code=200, content=data)

    # async def update(self, db: AsyncSession):
        
    #     data = response_api(200) 
        
    #     # update user basic profile data logic goes here 
        
    #     return JSONResponse(status_code=200, content=data)

    # async def update_avatar(self, db: AsyncSession):
        
    #     data = response_api(200) 
    #     # update user avatar logic goes here 
        
    #     return JSONResponse(status_code=200, content=data)
