from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date

from app.models.app_module import App_module
from app.models.app_action import App_action
from app.models.app_module_action import App_module_action
from app.models.user import User
from app.models.office import Office
from app.models.position import Position
from app.models.user_type import User_type
from app.models.user_type_access import User_type_access
from app.models.user_access import User_access

from app.utils.argon2_util import argon2_encrypt

class StarterRepository:

    # ---------- CHECK EXISTENCE ----------
    async def user_username_exist(self, db: AsyncSession, username: str) -> bool:
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return bool(result.scalar_one_or_none())

    # ---------- BULK INSERTS ----------
    async def bulk_module_insert(self, db: AsyncSession, modules: list[dict]):
        db.add_all([
            App_module(
                app_module_id=m["app_module_id"],
                name=m["name"],
                rank=m["rank"]
            )
            for m in modules
        ])

    async def bulk_action_insert(self, db: AsyncSession, actions: list[dict]):
        db.add_all([App_action(**a) for a in actions])

    async def bulk_module_action_insert(self, db: AsyncSession, modules: list[dict]):
        db.add_all([
            App_module_action(
                app_module_id=m["app_module_id"],
                app_action_id=action_id,
            )
            for m in modules
            for action_id in m.get("actions", [])
        ])

    # ---------- TEMP INSERTS ----------
    async def temp_new_office(self, db: AsyncSession, code: str, name: str) -> int:
        obj = Office(code=code, name=name, address="")
        db.add(obj)
        await db.flush()
        return obj.office_id

    async def temp_new_position(self, db: AsyncSession, code: str, name: str) -> int:
        obj = Position(code=code, name=name)
        db.add(obj)
        await db.flush()
        return obj.position_id

    async def temp_new_user_type(self, db: AsyncSession, name: str) -> int: 
        obj = User_type(name=name, description="", is_editable=0)
        db.add(obj)
        await db.flush()

        result = await db.execute(select(App_module_action.app_module_action_id))
        
        db.add_all( 
            User_type_access( 
                user_type_id=obj.user_type_id, 
                app_module_action_id=ma_id, 
                is_active=1 
            ) for ma_id in result.scalars() 
        ) 
        return obj.user_type_id 

    async def temp_new_user(
        self, 
        db: AsyncSession, 
        username: str, 
        user_type_id: int, 
        office_id: int, 
        position_id: int
    ) -> int:
        obj = User(
            user_type_id=user_type_id,
            office_id=office_id,
            position_id=position_id,
            username=username, 
            password=argon2_encrypt(username), 
            first_name=username, 
            middle_name="", 
            last_name=username, 
            gender=1, 
            birth_date=date(1997, 8, 16), 
            email= "", 
            email_otp="", 
            email_otp_valid_until=None, 
            status=1
        )
        db.add(obj)
        await db.flush()
        
        user_id = obj.user_id

        result = await db.execute(
            select(User_type_access.app_module_action_id)
            .where(User_type_access.user_type_id == user_type_id)
            .where(User_type_access.is_active == 1)
        ) 
        
        db.add_all(
            User_access(
                user_id=user_id,
                app_module_action_id=ma_id,
                is_active=1
            ) for ma_id in result.scalars()
        )
        
        return user_id
    
