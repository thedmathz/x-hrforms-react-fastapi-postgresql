from pydantic import BaseModel
from typing import Optional

class AuthenticationLogin(BaseModel):
    username: str
    password: str