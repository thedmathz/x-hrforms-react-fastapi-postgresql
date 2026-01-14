from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class Form_application(Base):
    __tablename__ = 'form_applications'

    form_application_id     = Column(INTEGER, nullable=False, primary_key=True) 
    form_type_id            = Column(SMALLINT, ForeignKey('form_types.form_type_id'), nullable=False) 
    user_id                 = Column(INTEGER, ForeignKey('users.user_id'), nullable=False) 
    leave_date_started      = Column(DATE, nullable=True) 
    leave_date_ended        = Column(DATE, nullable=True) 
    leave_number_of_hours   = Column(NUMERIC(4,1), nullable=False) 
    leave_reason            = Column(TEXT, nullable=False) 
    travel_date_started     = Column(TIMESTAMP(timezone=True), nullable=True) 
    travel_date_ended       = Column(TIMESTAMP(timezone=True), nullable=True) 
    travel_origin           = Column(TEXT, nullable=False) 
    travel_destinations     = Column(TEXT, nullable=False) 
    travel_cost             = Column(NUMERIC(12,2), nullable=False) 
    travel_reason           = Column(TEXT, nullable=False) 
    date_filed              = Column(TIMESTAMP(timezone=True), nullable=True) 
    recommender_user_id     = Column(INTEGER, ForeignKey('users.user_id'), nullable=False) 
    date_recommended        = Column(TIMESTAMP(timezone=True), nullable=True) 
    approver_user_id        = Column(INTEGER, ForeignKey('users.user_id'), nullable=False) 
    date_approved           = Column(TIMESTAMP(timezone=True), nullable=True) 
    status                  = Column(SMALLINT, nullable=False) 