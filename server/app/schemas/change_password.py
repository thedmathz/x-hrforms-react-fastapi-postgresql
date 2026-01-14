from pydantic import BaseModel
from typing import Optional

class ChangePasswordForm(BaseModel):
    password_current    : str
    password_new        : str
    password_confirm    : str