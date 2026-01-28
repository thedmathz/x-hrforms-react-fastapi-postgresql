from importlib.metadata.diagnose import inspect
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.orm import aliased
from sqlalchemy import select, insert, delete, update, inspect

from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.models.app_module import App_module
from app.models.app_action import App_action
from app.models.app_module_action import App_module_action
from app.models.office import Office
from app.models.position import Position
from app.models.user import User
from app.models.user_access import User_access
from app.models.user_type import User_type
from app.models.user_type_access import User_type_access 
from app.schemas.user import UserInsert

class UserRepository:
    
    async def _record_does_exist(self, db: AsyncSession, id: int):
        stmt = select(User).where(User.user_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() 

    async def index(self, db: AsyncSession):
        
        stmt = (
            select(
                User.user_id,
                User.username,
                User.first_name,
                User.middle_name,
                User.last_name,
                User_type.name.label("user_type_name"),
                Office.code.label("office_code"),
                Position.code.label("position_code"),
                User.status,
            )
            .outerjoin(User_type, User.user_type_id == User_type.user_type_id)
            .outerjoin(Office, User.office_id == Office.office_id)
            .outerjoin(Position, User.position_id == Position.position_id)
        )
        
        result = await db.execute(stmt)
        return result.mappings().all()

    async def get_module_action_id_by_name(self, db: AsyncSession, module_name: str, action_name: str):
        stmt = (
            select(
                App_module_action.app_module_action_id,        
            )
            .select_from(App_module_action)
            .join(App_module, App_module_action.app_module_id == App_module.app_module_id, isouter = True)
            .join(App_action, App_module_action.app_action_id == App_action.app_action_id, isouter = True)
            .where(App_module.name == module_name)
            .where(App_action.name == action_name)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_types(self, db: AsyncSession):
        stmt = select(
            User_type.user_type_id,
            User_type.name,
        ).order_by(User_type.name.asc())
        result = await db.execute(stmt)
        return result.mappings().all()

    async def get_offices(self, db: AsyncSession):
        stmt = select(
            Office.office_id,
            Office.code,
            Office.name,
        ).order_by(Office.code.asc())
        result = await db.execute(stmt)
        return result.mappings().all()

    async def get_positions(self, db: AsyncSession):
        stmt = select(
            Position.position_id,
            Position.code,
            Position.name,
        ).order_by(Position.code.asc())
        result = await db.execute(stmt)
        return result.mappings().all()

    async def get_recommenders(self, db: AsyncSession, recommender_app_module_action_id: int): 
        
        subquery = (
            select(User_access.user_id)
            .where(User_access.app_module_action_id == recommender_app_module_action_id)
            .where(User_access.is_active == 1)
        )
        
        stmt = select(
            User.user_id,
            User.username,
            User.first_name,
            User.middle_name,
            User.last_name,
        ).where(
            User.user_id.in_(subquery)
        ).order_by(
            User.last_name.asc(), 
            User.first_name.asc(), 
        )
        result = await db.execute(stmt)
        return result.mappings().all()

    async def get_approvers(self, db: AsyncSession, approver_app_module_action_id: int):
        
        subquery = (
            select(User_access.user_id)
            .where(User_access.app_module_action_id == approver_app_module_action_id)
            .where(User_access.is_active == 1)
        )
        
        stmt = select(
            User.user_id,
            User.username,
            User.first_name,
            User.middle_name,
            User.last_name,
        ).where(
            User.user_id.in_(subquery)
        ).order_by(
            User.last_name.asc(), 
            User.first_name.asc(), 
        )
        result = await db.execute(stmt)
        return result.mappings().all()
    
    async def validate_username_unique(self, db: AsyncSession, username: str, user_id: int = None) -> bool:
        stmt = select(User).where(User.username == username) 
        if user_id:
            stmt = stmt.where(User.user_id != user_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is None 

    async def validate_recommender_approver_ids(self, db: AsyncSession, recommender_id: int, recommender_app_module_action_id: int, approver_id: int, approver_app_module_action_id: int) -> bool:
        
        is_valid = True 
        
        if is_valid and (not recommender_id or not approver_id): 
            is_valid = False 
            
        if is_valid:
            result = await db.execute(
                select(User_access)
                .where(User_access.is_active == 1) 
                .where(User_access.user_id == recommender_id) 
                .where(User_access.app_module_action_id == recommender_app_module_action_id)
            )
            if not result.scalar_one_or_none():
                is_valid = False 
            
        if is_valid:
            result = await db.execute(
                select(User_access)
                .where(User_access.is_active == 1) 
                .where(User_access.user_id == approver_id) 
                .where(User_access.app_module_action_id == approver_app_module_action_id)
            )
            if not result.scalar_one_or_none():
                is_valid = False 
        
        return is_valid 

    async def insert(self, db: AsyncSession, form_request: UserInsert, password: str):
        
        stmt = (
            insert(User)
            .values(
                user_type_id        = form_request.user_type_id,
                office_id           = form_request.office_id,
                position_id         = form_request.position_id,
                username            = form_request.username,
                password            = password,
                first_name          = "",
                middle_name         = "",
                last_name           = "",
                gender              = 1,
                recommender_id      = form_request.recommender_id,
                approver_id         = form_request.approver_id,
                email               = form_request.email,
                email_otp           = "",
                forgot_password_otp = "",
                picture_path        = "",
                status              = 0
            )
            .returning(User.user_id)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()

    async def view(self, db: AsyncSession, user_id: int): 
        
        Recommender = aliased(User)
        Approver = aliased(User)
        
        result = await db.execute(
            select(
                User_type.name.label("user_type_name"),        
                User.username,        
                User.first_name,        
                User.middle_name,        
                User.last_name,        
                User.gender,        
                User.birth_date,        
                User.email,        
                Office.code.label("office_code"), 
                Office.name.label("office_name"), 
                Position.code.label("position_code"),        
                Position.name.label("position_name"), 
                User.recommender_id,        
                Recommender.last_name.label("recommender_last_name"), 
                Recommender.first_name.label("recommender_first_name"), 
                Recommender.middle_name.label("recommender_middle_name"), 
                User.approver_id,        
                Approver.last_name.label("approver_last_name"), 
                Approver.first_name.label("approver_first_name"), 
                Approver.middle_name.label("approver_middle_name"), 
                User.status,        
            )
            .select_from(User)
            .join(User_type, User.user_type_id == User_type.user_type_id, isouter = True)
            .join(Office, User.office_id == Office.office_id, isouter = True)
            .join(Position, User.position_id == Position.position_id, isouter = True)
            .join(Recommender, User.recommender_id == Recommender.user_id, isouter = True)
            .join(Approver, User.approver_id == Approver.user_id, isouter = True)
            .where(User.user_id == user_id)
        )
        return result.mappings().one_or_none()

    async def is_admin_username(self, db: AsyncSession, user_id: int) -> bool: 
        stmt = (
            select(User)
            .where(User.username == "admin")
            .where(User.user_id == user_id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() 

    async def is_user_pending(self, db: AsyncSession, user_id: int) -> bool: 
        stmt = (
            select(User)
            .where(User.user_id == user_id)
            .where(User.status == 0)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() 

    async def update_status(self, db: AsyncSession, user_id: int, status: int): 
        
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(status=status)
        )
        await db.execute(stmt)
        await db.commit()

    async def update(self, db: AsyncSession, obj: Position): 
        await db.commit()
        await db.refresh(obj) 
        return obj.user_id
    