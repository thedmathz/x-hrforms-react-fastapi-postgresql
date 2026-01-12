from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.position_service import PositionService

from app.schemas.position import PositionInsert, PositionUpdate

from app.utils.argon2_util import argon2_encrypt

router  = APIRouter()
service = PositionService()

@router.get("/")
async def index(db: AsyncSession = Depends(get_db)):
    return await service.index(db)

@router.post("/")
async def insert(form_request: PositionInsert, db: AsyncSession = Depends(get_db)):
    return await service.insert(db, form_request) 

@router.get("/argon2")
async def argon2(db: AsyncSession = Depends(get_db)):
    return {"status": argon2_encrypt("sadwaw")}

@router.get("/{id}")
async def view(id: str, db: AsyncSession = Depends(get_db)):
    return await service.view(db, id) 

@router.put("/{id}")
async def update(id: str, form_request: PositionUpdate, db: AsyncSession = Depends(get_db)):
    return await service.update(db, id, form_request)

@router.delete("/{id}")
async def delete(id: str, db: AsyncSession = Depends(get_db)):
    return await service.delete(db, id)
