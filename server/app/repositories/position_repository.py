from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.position import Position
from app.schemas.position import PositionGetRow

class PositionRepository:

    '''
    Specific helper methods
    '''
    async def _record_does_exist(self, db: AsyncSession, id: int):
        stmt = select(Position).where(Position.position_id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none() 

    '''
    Common CRUD operations
    '''
    async def index(self, db: AsyncSession):
        query = select(Position)
        result = await db.execute(query)
        return result.scalars().all()

    async def insert(self, db: AsyncSession, obj: Position):
        db.add(obj)
        await db.commit()
        await db.refresh(obj) 
        return obj.position_id
    
    async def view(self, db: AsyncSession, id: int) -> PositionGetRow:
        result = await db.execute(
            select(
                Position.code,
                Position.name,
            ).where(Position.position_id == id)
        )
        return result.mappings().one_or_none()

    async def update(self, db: AsyncSession, obj: Position): 
        await db.commit()
        await db.refresh(obj) 
        return obj.position_id

    async def delete(self, db: AsyncSession, obj: Position): 
        await db.delete(obj)
        return await db.commit()

