from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse 
from app.repositories.position_repository import PositionRepository
from app.models.position import Position
from app.schemas.position import PositionInsert, PositionUpdate
from app.utils.fernet_util import fernet_encrypt, fernet_decrypt
from app.utils.response_util import response_api

class PositionService:
    
    def __init__(self): self.repo = PositionRepository()

    async def index(self, db: AsyncSession):
        
        data = response_api(200) 
        
        records = []
    
        temp_records = await self.repo.index(db) 
        for row in temp_records:
            records.append({
                "id": fernet_encrypt(str(row.position_id)).decode(), 
                "code": row.code, 
                "name": row.name, 
            })
            
        data['records'] = records

        return JSONResponse(status_code=200, content=data)

    async def insert(self, db: AsyncSession, form_request: PositionInsert):
        
        data = response_api(200) 
        
        # Validation
        if form_request.code == "":
            response_api(400, "Code is required", "Invalid")
        
        obj = Position(**form_request.model_dump()) 
        position_id = await self.repo.insert(db, obj) 
    
        data['id'] = position_id

        return JSONResponse(status_code=200, content=data)

    async def view(self, db: AsyncSession, id: str):
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        row = await self.repo.view(db, row_id) 
        if row:
            data['row'] = {
                'code': row.code,
                'name': row.name,
            }
            
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)

    async def update(self, db: AsyncSession, id: str, form_request: PositionUpdate):
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        # Validation
        if form_request.code == "":
            response_api(400, "Code is required", "Invalid")
        
        obj = await self.repo._record_does_exist(db, row_id)
        if not obj:
            response_api(400, "Record not found", "Invalid")
        
        # Apply changes in API or in service
        for field, value in form_request.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        
        position_id = await self.repo.update(db, obj)
        
        data['id'] = position_id

        return JSONResponse(status_code=200, content=data)

    async def delete(self, db: AsyncSession, id: str):
        
        row_id = int(fernet_decrypt(id))
        
        data = response_api(200) 
        
        obj = await self.repo._record_does_exist(db, row_id)
        if not obj:
            response_api(400, "Record not found", "Invalid")
        
        await self.repo.delete(db, obj)
        
        data['id'] = id
        
        return JSONResponse(status_code=200, content=data)
