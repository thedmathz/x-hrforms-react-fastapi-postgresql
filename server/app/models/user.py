from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class User(Base):
    __tablename__ = 'users'

    user_id                 = Column(INTEGER, nullable=False, primary_key=True) 
    user_type_id            = Column(SMALLINT, ForeignKey('user_types.user_type_id'), nullable=False) 
    office_id               = Column(SMALLINT, ForeignKey('offices.office_id'), nullable=False) 
    position_id             = Column(SMALLINT, ForeignKey('positions.position_id'), nullable=False) 
    username                = Column(VARCHAR(50), nullable=False) 
    password                = Column(TEXT, nullable=False) 
    first_name              = Column(VARCHAR(30), nullable=False) 
    middle_name             = Column(VARCHAR(30), nullable=False) 
    last_name               = Column(VARCHAR(30), nullable=False) 
    gender                  = Column(SMALLINT, nullable=False) 
    birth_date              = Column(DATE, nullable=True) 
    email                   = Column(TEXT, nullable=False) 
    email_otp               = Column(VARCHAR(6), nullable=False) 
    email_otp_valid_until   = Column(TIMESTAMP, nullable=True) 
    status                  = Column(SMALLINT, nullable=False) 