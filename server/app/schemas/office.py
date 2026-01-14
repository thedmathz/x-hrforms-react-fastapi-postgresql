from pydantic import BaseModel
from typing import Optional

class OfficeGetRow(BaseModel):
    code    : str
    name    : str
    address : str

class OfficeGetRowWithId(OfficeGetRow):
    office_id : int

class OfficeGetRowsList(BaseModel):
    records: list[OfficeGetRowWithId] 
    
class OfficeInsert(BaseModel):
    code: str
    name: str
    address: str

class OfficeUpdate(OfficeInsert): pass