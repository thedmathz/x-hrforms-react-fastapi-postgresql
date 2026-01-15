from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from app.models.user_type import User_type
from app.schemas.my_profile import MyProfileGetRow

class MyProfileRepository:

    async def index(self, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(
                User.user_id,
                User.username,
                User.first_name,
                User.middle_name,
                User.last_name,
                User.gender,
                User.birth_date,
                User_type.name.label("user_type_name"),
            )
            .select_from(User)
            .outerjoin(User_type, User.user_type_id == User_type.user_type_id)
            .where(User.user_id == user_id)
        )
        return result.mappings().one_or_none()

    # async def edit(self, db: AsyncSession, id: int) -> OfficeGetRow:
    #     result = await db.execute(
    #         select(
    #             Office.code,
    #             Office.name,
    #             Office.address,
    #         ).where(Office.office_id == id)
    #     )
    #     return result.mappings().one_or_none()

    # async def update(self, db: AsyncSession, obj: Office): 
    #     await db.commit()
    #     await db.refresh(obj) 
    #     return obj.office_id
