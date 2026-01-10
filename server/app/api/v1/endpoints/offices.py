from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def index():
    return {"key": "element"}

@router.get("/add")
async def add():
    return {"key": "element"}

@router.post("/")
async def insert():
    return {"key": "element"}

@router.get("/{id}")
async def view(id: str):
    return {"key": "element"}

@router.get("/{id}/edit")
async def edit(id: str):
    return {"key": "element"}

@router.put("/{id}")
async def update(id: str):
    return {"key": "element"}

@router.delete("/{id}")
async def delete(id: str):
    return {"key": "element"}
