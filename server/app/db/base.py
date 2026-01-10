# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# IMPORTANT: import all models here
# from app.models.user import User
# from app.models.product import Product
