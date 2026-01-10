from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def index():
    return {"key": "element"}

@router.get("/print-list")
async def print_list():
    return {"key": "element"}

@router.get("/{id}")
async def view(id: str):
    return {"key": "element"}

@router.get("/{id}/recommend")
async def recommend(id: str):
    return {"key": "element"}

@router.get("/{id}/approve")
async def approve(id: str):
    return {"key": "element"}

@router.get("/{id}/print-request")
async def print_request(id: str):
    return {"key": "element"}

# @router.get("/{user_id}")
# async def get_user(user_id: int):
#     return {
#         "user_id": user_id,
#         "name": "John Doe"
#     }
