from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.starter_service import StarterService

router  = APIRouter()
service = StarterService()

@router.get("/")
async def index(db: AsyncSession = Depends(get_db)):
    return await service.index(db)
