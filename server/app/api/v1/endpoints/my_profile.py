from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.core.dependencies import get_current_user

from app.services.my_profile_service import MyProfileService

router = APIRouter()
service = MyProfileService()

@router.get("/")
async def index(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    return await service.index(db, int(current_user_id))

# @router.get("/edit")
# async def edit(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
#     return await service.edit(db)

# @router.post("/update")
# async def update(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
#     return await service.update(db)

# @router.post("/update-avatar")
# async def update_avatar(db: AsyncSession = Depends(get_db), current_user_id: str = Depends(get_current_user)):
#     return await service.update_avatar(db)