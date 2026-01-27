from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_type import UserTypeInsert, UserTypeUpdate
from app.db.session import get_db

from app.core.dependencies import get_current_user

from app.services.user_type_service import UserTypeService

router = APIRouter()
service = UserTypeService()

@router.get("/")
async def index(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.index(db)

@router.get("/add")
async def add(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.add(db)

@router.post("/")
async def insert(form_request: UserTypeInsert, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.insert(db, form_request)

@router.get("/{id}")
async def view(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.view(db, id)

@router.get("/{id}/edit")
async def edit(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.edit(db, id)

@router.put("/{id}")
async def update(id: str, form_request: UserTypeUpdate, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.update(db, id, form_request)

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.delete(db, id)