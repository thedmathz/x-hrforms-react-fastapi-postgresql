from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.office import Office
from app.schemas.office import OfficeGetRow

class OfficeRepository:

    '''
    Specific helper methods
    '''
    async def _record_does_exist(self, db: AsyncSession, id: int):
        stmt = select(Office).where(Office.office_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() 

    '''
    Common CRUD operations
    '''
    async def index(self, db: AsyncSession):
        query = select(Office)
        result = await db.execute(query)
        return result.scalars().all()

    async def insert(self, db: AsyncSession, obj: Office):
        db.add(obj)
        await db.commit()
        await db.refresh(obj) 
        return obj.office_id

    async def view(self, db: AsyncSession, id: int) -> OfficeGetRow:
        result = await db.execute(
            select(
                Office.code,
                Office.name,
                Office.address,
            ).where(Office.office_id == id)
        )
        return result.mappings().one_or_none()

    async def update(self, db: AsyncSession, obj: Office): 
        await db.commit()
        await db.refresh(obj) 
        return obj.office_id

    async def delete(self, db: AsyncSession, obj: Office): 
        await db.delete(obj)
        return await db.commit()

