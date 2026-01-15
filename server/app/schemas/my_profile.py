from pydantic import BaseModel
from typing import Optional

class MyProfileGetRow(BaseModel):
    code    : str
    name    : str

class MyProfileGetRowWithId(MyProfileGetRow):
    my_profile_id : int

class MyProfileGetRowsList(BaseModel):
    records: list[MyProfileGetRowWithId] 
    
class MyProfileInsert(BaseModel):
    code: str
    name: str

class MyProfileUpdate(MyProfileInsert): pass