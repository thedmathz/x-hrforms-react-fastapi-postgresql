from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class Token(Base):
    __tablename__ = 'tokens'

    token_id            = Column(INTEGER, nullable=False, primary_key=True) 
    user_id             = Column(INTEGER, ForeignKey('users.user_id'), nullable=False) 
    username            = Column(VARCHAR(50), nullable=False) 
    token               = Column(TEXT, nullable=False) 
    date_started        = Column(TIMESTAMP, nullable=True) 
    date_stopped        = Column(TIMESTAMP, nullable=True) 
    date_expiration     = Column(TIMESTAMP, nullable=True) 
    time_minute_used    = Column(SMALLINT, nullable=False) 
    time_minute_total   = Column(SMALLINT, nullable=False) 
    is_active           = Column(SMALLINT, nullable=False) 