from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.events import (
    create_start_app_handler, 
    create_stop_app_handler
)

app = FastAPI(title="HR Forms")

app.include_router(api_router)

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))
