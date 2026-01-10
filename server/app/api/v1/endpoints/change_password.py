from fastapi import APIRouter

router = APIRouter()

@router.get("/update")
async def update():
    return {"key": "element"}
