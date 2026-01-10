from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def login():
    return {"key": "element"}

@router.get("/refresh")
async def refresh():
    return {"key": "element"}

@router.get("/me")
async def me():
    return {"key": "element"}

@router.get("/logout")
async def logout():
    return {"key": "element"}
