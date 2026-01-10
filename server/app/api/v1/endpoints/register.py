from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def index():
    return {"key": "element"}

@router.get("/update")
async def update():
    return {"key": "element"}
