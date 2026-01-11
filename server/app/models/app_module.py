from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class App_module(Base):
    __tablename__ = 'app_modules'

    app_module_id   = Column(SMALLINT, nullable=False, primary_key=True) 
    name            = Column(VARCHAR(25), nullable=False) 
    rank            = Column(SMALLINT, nullable=False) 