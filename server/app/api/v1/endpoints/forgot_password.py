from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.services.forgot_password_service import ForgotPasswordService 
from app.schemas.forgot_password import ForgotPasswordUsername, ForgotPasswordOtp, ForgotPasswordReset

router = APIRouter()
service = ForgotPasswordService()

@router.post("/check-username")
async def check_username(form_request: ForgotPasswordUsername, db: AsyncSession = Depends(get_db)):
    return await service.check_username(db, form_request)

@router.post("/{code}/resend-otp")
async def resend_otp(code: str, db: AsyncSession = Depends(get_db)):
    return await service.resend_otp(db, code)

# otp
@router.get("/{code}/otp")
async def otp(code: str, db: AsyncSession = Depends(get_db)):
    return await service.otp(db, code)

@router.post("/{code}/check-otp")
async def check_otp(form_request: ForgotPasswordOtp, code: str, db: AsyncSession = Depends(get_db)):
    return await service.check_otp(db, code, form_request) 

# reset password
@router.get("/{code}/reset-password") 
async def reset_password(code: str, db: AsyncSession = Depends(get_db)):
    return await service.reset_password(db, code)

@router.post("/{code}/check-reset-password")
async def check_reset_password(form_request: ForgotPasswordReset, code: str, db: AsyncSession = Depends(get_db)):
    return await service.check_reset_password(db, code, form_request) 


