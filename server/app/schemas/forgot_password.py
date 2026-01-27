from pydantic import BaseModel
from typing import Optional
from datetime import date

class ForgotPasswordUsername(BaseModel): 
    username: str 

class ForgotPasswordOtp(BaseModel): 
    forgot_password_otp: str

class ForgotPasswordReset(BaseModel): 
    password_new        : str
    password_confirm    : str