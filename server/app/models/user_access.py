from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class User_access(Base):
    __tablename__ = 'user_accesses'

    user_access_id          = Column(INTEGER, nullable=False, primary_key=True) 
    user_id                 = Column(INTEGER, ForeignKey('users.user_id'), nullable=False) 
    app_module_action_id    = Column(SMALLINT, ForeignKey('app_module_actions.app_module_action_id'), nullable=False) 
    is_active               = Column(SMALLINT, nullable=False) 