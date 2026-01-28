from pydantic import BaseModel 
from typing import Optional

class UserGetRow(BaseModel):
    name        : str
    description : str

class UserInsert(BaseModel):
    user_type_id    : int 
    username        : Optional[str] = ""
    email           : str
    office_id       : int 
    position_id     : int 
    recommender_id  : int
    approver_id     : int

class UserUpdate(UserInsert): pass 