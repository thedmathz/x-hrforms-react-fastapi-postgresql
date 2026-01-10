from fastapi import APIRouter

router = APIRouter()

@router.get("/cards")
async def cards():
    return {"key": "element"}

@router.get("/gender-distribution")
async def gender_distribution():
    return {"key": "element"}

@router.get("/monthly-employees")
async def monthly_employees():
    return {"key": "element"}

@router.get("/latest-applications")
async def latest_applications():
    return {"key": "element"}

