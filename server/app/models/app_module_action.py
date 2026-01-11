from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class App_module_action(Base):
    __tablename__ = 'app_module_actions'

    app_module_action_id    = Column(INTEGER, nullable=False, primary_key=True) 
    app_module_id           = Column(SMALLINT, ForeignKey('app_modules.app_module_id'), nullable=False) 
    app_action_id           = Column(SMALLINT, ForeignKey('app_actions.app_action_id'), nullable=False) 