from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models.app_action import App_action
from app.models.app_module_action import App_module_action
from app.models.app_module import App_module
from app.models.form_application import Form_application
from app.models.form_type import Form_type
from app.models.office import Office
from app.models.position import Position
from app.models.token import Token
from app.models.user_access import User_access
from app.models.user_type_access import User_type_access
from app.models.user_type import User_type
from app.models.user import User