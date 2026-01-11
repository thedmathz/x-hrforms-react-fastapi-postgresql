from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class Office(Base):
    __tablename__ = 'offices'

    office_id   = Column(INTEGER, nullable=False, primary_key=True) 
    code        = Column(VARCHAR(10), nullable=False) 
    name        = Column(VARCHAR(100), nullable=False) 
    address     = Column(TEXT, nullable=False) 