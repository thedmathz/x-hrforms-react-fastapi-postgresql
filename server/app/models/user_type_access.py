from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class User_type_access(Base):
    __tablename__ = 'user_type_accesses'

    user_type_access_id    = Column(INTEGER, nullable=False, primary_key=True) 
    user_type_id           = Column(SMALLINT, ForeignKey('user_types.user_type_id'), nullable=False) 
    app_module_action_id   = Column(SMALLINT, ForeignKey('app_module_actions.app_module_action_id'), nullable=False) 
    is_active              = Column(SMALLINT, nullable=False) 