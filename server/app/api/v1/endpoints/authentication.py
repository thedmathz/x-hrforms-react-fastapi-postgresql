from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.core.dependencies import get_current_user, get_refresh_current_user

from app.services.authentication_service import AuthenticationService
from app.schemas.authentication import AuthenticationLogin

router = APIRouter()
service = AuthenticationService()

@router.post("/login") 
async def login(form_request: AuthenticationLogin, db: AsyncSession = Depends(get_db)):
    return await service.login(db, form_request) 

@router.get("/me")
async def me(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.me(db, int(current_user_id)) 

@router.post("/refresh")
async def refresh(db: AsyncSession = Depends(get_db), context: str = Depends(get_refresh_current_user)):
    return await service.refresh(db, context) 

@router.post("/logout")
async def logout(db: AsyncSession = Depends(get_db), token: str = Cookie(None)):
    return await service.logout(db, token)
