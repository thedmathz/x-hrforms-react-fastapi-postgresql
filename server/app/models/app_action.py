from sqlalchemy import Column, ForeignKey
from app.db.base import Base
from sqlalchemy.dialects.postgresql import (
    SMALLINT, INTEGER, BIGINT, NUMERIC, 
    VARCHAR, TEXT, 
    DATE, TIME, TIMESTAMP, 
)

class App_action(Base):
    __tablename__ = 'app_actions'

    app_action_id   = Column(SMALLINT, nullable=False, primary_key=True) 
    name            = Column(VARCHAR(25), nullable=False) 
    rank            = Column(SMALLINT, nullable=False) 