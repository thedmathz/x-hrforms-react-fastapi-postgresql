import asyncio
import json

from datetime import date
from pathlib import Path
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.argon2_util import argon2_encrypt

from app.models.user import User
from app.models.user_access import User_access
from app.models.user_type import User_type
from app.models.user_type_access import User_type_access
from app.models.office import Office
from app.models.position import Position 

async def create_user_admin(db: AsyncSession, user_type_id: int, office_id: int, position_id: int):
    print("\n🌱 Insert USER...")
    
    username = "admin"
    
    # insert user
    user = User(
        user_type_id            = user_type_id,
        office_id               = office_id,
        position_id             = position_id,
        username                = username, 
        password                = argon2_encrypt(username), 
        first_name              = username, 
        middle_name             = "", 
        last_name               = username, 
        gender                  = 1, 
        birth_date              = date(1997, 8, 16), 
        email                   = "", 
        email_otp               = "", 
        email_otp_valid_until   = None, 
        forgot_password_otp     = "", 
        picture_path            = "", 
        status                  = 1
    )
    db.add(user)
    await db.flush()
    user_id = user.user_id
    
    # get all module actions for this user type
    result = await db.execute(
        select(User_type_access.app_module_action_id)
        .where(User_type_access.user_type_id == user_type_id)
        .where(User_type_access.is_active == 1)
    ) 
    
    # insert user access here
    db.add_all(
        User_access(
            user_id=user_id,
            app_module_action_id=ma_id,
            is_active=1
        ) for ma_id in result.scalars()
    )
    
    print("✅ Insert USER complete!")

if __name__ == "__main__":
    asyncio.run(create_user_admin())
