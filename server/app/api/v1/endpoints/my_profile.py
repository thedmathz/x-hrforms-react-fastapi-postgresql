from fastapi import APIRouter, UploadFile, File, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.core.dependencies import get_current_user

from app.services.my_profile_service import MyProfileService 
from app.schemas.my_profile import MyProfileUpdate, MyProfileEmailOtp, MyProfileEmailUpdate

router = APIRouter()
service = MyProfileService()

@router.get("/")
async def index(request: Request, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.index(request, db, int(current_user_id)) 

@router.get("/edit")
async def edit(request: Request, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.edit(request, db, int(current_user_id)) 

@router.post("/update") 
async def update(form_request: MyProfileUpdate, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)): 
    return await service.update(db, form_request, int(current_user_id)) 

@router.get("/edit-email") 
async def edit_email(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)): 
    return await service.edit_email(db, int(current_user_id)) 

@router.post("/set-email-otp") 
async def set_email_otp(form_request: MyProfileEmailOtp, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)): 
    return await service.set_email_otp(db, form_request, int(current_user_id)) 

@router.post("/update-email") 
async def update_email(form_request: MyProfileEmailUpdate, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)): 
    return await service.update_email(db, form_request, int(current_user_id)) 

@router.post("/update-avatar")
async def update_avatar(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.update_avatar(db, current_user_id, file)