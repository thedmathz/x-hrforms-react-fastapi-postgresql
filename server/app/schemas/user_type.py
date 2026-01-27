from pydantic import BaseModel
from typing import List

class UserTypeGetRow(BaseModel):
    name        : str
    description : str

class UserTypeInsert(UserTypeGetRow):
    name                    : str
    description             : str
    app_module_action_ids   : List[int]

class UserTypeUpdate(UserTypeInsert): pass