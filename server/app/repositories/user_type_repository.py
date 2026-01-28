from importlib.metadata.diagnose import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update, inspect

from app.models.app_module import App_module
from app.models.app_action import App_action
from app.models.app_module_action import App_module_action
from app.models.user_type import User_type
from app.models.user_type_access import User_type_access 
from app.schemas.user_type import UserTypeGetRow

class UserTypeRepository:

    async def _record_does_exist(self, db: AsyncSession, id: int):
        stmt = select(User_type).where(User_type.user_type_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() 

    async def validate_user_type_name_unique(self, db: AsyncSession, name: str, user_type_id: int = None) -> bool:
        stmt = select(User_type).where(User_type.name == name) 
        if user_type_id:
            stmt = stmt.where(User_type.user_type_id != user_type_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is None

    async def index(self, db: AsyncSession):
        result = await db.execute( select(User_type) )
        return result.scalars().all()

    async def get_app_modules(self, db: AsyncSession):
        
        subquery = (
            select(App_module_action.app_module_id)
            .where(App_module_action.app_action_id == 1)
        )
        
        result = await db.execute(
            select(App_module)
            .where(App_module.app_module_id.in_(subquery))
            .order_by(App_module.rank.asc())
        ) 
        
        return result.scalars().all() 

    async def get_app_actions_by_module_id(self, db: AsyncSession, app_module_id: int):
        
        result = await db.execute(
            select(
                App_module_action.app_module_action_id,        
                App_action.name,        
            )
            .select_from(App_module_action)
            .join(
                App_action, 
                App_module_action.app_action_id == App_action.app_action_id, 
                isouter = True
            )
            .where(App_module_action.app_module_id == app_module_id)
            .order_by(App_action.rank.asc())
        ) 
        
        return result.mappings().all() 

    async def insert(self, db: AsyncSession, name: str, description: str):
        obj = User_type(
            name        = name, 
            description = description, 
            is_editable = 1
        )
        db.add(obj) 
        await db.commit() 
        await db.refresh(obj) 
        return obj.user_type_id 

    async def validate_app_module_action_ids(self, db: AsyncSession, app_module_action_ids: list[int]):
        # Get existing IDs from the table
        result = await db.execute(
            select(App_module_action.app_module_action_id)
            .where(App_module_action.app_module_action_id.in_(app_module_action_ids))
        )
        existing_ids = set(result.scalars().all())  # convert to set for uniqueness

        # Check if all input IDs exist
        return all(i in existing_ids for i in app_module_action_ids)

    async def bulk_user_type_access_insert(self, db: AsyncSession, user_type_id: int, app_module_action_ids: list):
        values = [
            {"user_type_id": user_type_id, "app_module_action_id": action_id, "is_active": 1}
            for action_id in app_module_action_ids
        ]
        await db.execute(insert(User_type_access), values)
        await db.commit()

    async def view(self, db: AsyncSession, id: int) -> UserTypeGetRow:
        result = await db.execute(
            select(
                User_type.name,
                User_type.description,
            ).where(User_type.user_type_id == id)
        )
        return result.mappings().one_or_none()

    async def get_user_type_access_rights(self, db: AsyncSession, id: int) -> UserTypeGetRow:
        result = await db.execute(
            select(
                User_type_access.app_module_action_id,
            )
            .where(User_type_access.user_type_id == id)
            .where(User_type_access.is_active == 1)
        )
        return result.mappings().all()

    async def update(self, db: AsyncSession, obj: User_type): 
        await db.commit()
        await db.refresh(obj) 
        return obj.user_type_id

    async def bulk_user_type_access_deactivate(self, db: AsyncSession, user_type_id: int): 
        await db.execute(
            update(User_type_access)
            .where(User_type_access.user_type_id == user_type_id)
            .values(is_active = 0)
        )
        await db.commit()

    async def user_type_access_record_does_exist(self, db: AsyncSession, user_type_id: int, app_module_action_id: int): 
        result = await db.execute(
            select(User_type_access) 
            .where(User_type_access.user_type_id == user_type_id) 
            .where(User_type_access.app_module_action_id == app_module_action_id) 
        )
        return result.scalar_one_or_none() or None
        
    async def save_user_type_access(self, db: AsyncSession, obj: User_type_access): 
        if inspect(obj).transient:   # <-- object not in session yet
            db.add(obj)
        await db.commit()
        return obj.user_type_access_id

    async def delete(self, db: AsyncSession, obj: User_type): 
        await db.delete(obj)
        await db.commit()

    async def bulk_user_type_access_delete(self, db: AsyncSession, user_type_id: int): 
        await db.execute(
            delete(User_type_access)
            .where(User_type_access.user_type_id == user_type_id)                 
        )
        await db.commit()

        