from pydantic import BaseModel
from typing import Optional

class PositionGetRow(BaseModel):
    code    : str
    name    : str
    
class PositionGetRowWithId(PositionGetRow):
    position_id : int

class PositionGetRowsList(BaseModel):
    records: list[PositionGetRowWithId] 
    
class PositionInsert(BaseModel):
    code: str
    name: str

class PositionUpdate(PositionInsert): pass