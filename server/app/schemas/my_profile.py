from pydantic import BaseModel
from typing import Optional
from datetime import date

class MyProfileUpdate(BaseModel): 

    first_name: str 
    middle_name: str 
    last_name: str 
    gender: int 
    birth_date: date 

class MyProfileEmailOtp(BaseModel): 
    email: str

class MyProfileEmailUpdate(MyProfileEmailOtp): 
    email_otp: str