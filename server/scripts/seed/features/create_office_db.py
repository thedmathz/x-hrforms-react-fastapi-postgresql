import asyncio
import json

from pathlib import Path
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.office import Office

async def create_office(db: AsyncSession):
    print("\n🌱 Insert OFFICE...")
    
    office_code = "HQ"
    office_name = "Headquarters"
    
    office = Office(
        code=office_code, 
        name=office_name, 
        address=""
    )
    db.add(office)
    await db.flush()
    
    print("✅ Insert OFFICE complete!")
    return office.office_id

if __name__ == "__main__":
    asyncio.run(create_office())
