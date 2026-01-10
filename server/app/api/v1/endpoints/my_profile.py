from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def index():
    return {"key": "element"}

@router.get("/edit")
async def edit():
    return {"key": "element"}

@router.get("/update")
async def update():
    return {"key": "element"}

@router.get("/update-avatar")
async def update_avatar():
    return {"key": "element"}