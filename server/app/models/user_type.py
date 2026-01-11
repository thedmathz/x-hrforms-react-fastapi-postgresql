from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class User_type(Base):
    __tablename__ = 'user_types'

    user_type_id    = Column(SMALLINT, nullable=False, primary_key=True) 
    name            = Column(VARCHAR(25), nullable=False) 
    description     = Column(TEXT, nullable=False) 
    is_editable     = Column(SMALLINT, nullable=False) 