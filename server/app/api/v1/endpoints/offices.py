from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.core.dependencies import get_current_user

from app.services.office_service import OfficeService
from app.schemas.office import OfficeInsert, OfficeUpdate

router  = APIRouter()
service = OfficeService()

@router.get("/") 
async def index(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.index(db)

@router.post("/")
async def insert(form_request: OfficeInsert, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.insert(db, form_request) 

@router.get("/{id}")
async def view(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.view(db, id) 

@router.put("/{id}")
async def update(id: str, form_request: OfficeUpdate, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.update(db, id, form_request)

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.delete(db, id)
