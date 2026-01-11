from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class Form_type(Base):
    __tablename__ = 'form_types'

    form_type_id    = Column(SMALLINT, nullable=False, primary_key=True) 
    name            = Column(VARCHAR(25), nullable=False) 