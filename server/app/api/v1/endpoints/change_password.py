from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.core.dependencies import get_current_user

from app.services.change_password_service import ChangePasswordService
from app.schemas.change_password import ChangePasswordForm

router  = APIRouter()
service = ChangePasswordService()

@router.post("/")
async def index(form_request: ChangePasswordForm, db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.index(db, form_request, current_user_id)
