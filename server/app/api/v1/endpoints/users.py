from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user

from app.services.user_service import UserService
from app.schemas.user import UserInsert, UserUpdate

router = APIRouter()
service = UserService()

@router.get("/")
async def index(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.index(db)

@router.get("/add")
async def add(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.add(db)

@router.post("/")
async def insert(form_request: UserInsert, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.insert(db, form_request)

@router.get("/{id}")
async def view(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.view(db, id) 

@router.get("/{id}/edit")
async def edit(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.edit(db, id) 

@router.put("/{id}")
async def update(id: str, form_request: UserUpdate, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.update(db, id, form_request) 

@router.put("/{id}/activate")
async def activate(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.activate(db, id)

@router.put("/{id}/deactivate")
async def deactivate(id: str, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.deactivate(db, id)