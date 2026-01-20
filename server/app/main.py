from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.events import (
    create_start_app_handler, 
    create_stop_app_handler
)

is_prod = settings.ENVIRONMENT == "production"

app = FastAPI(
    title       = settings.PROJECT_NAME,
    version     = settings.PROJECT_VERSION, 
    docs_url    = None if is_prod else "/docs",
    redoc_url   = None if is_prod else "/redoc",
    openapi_url = None if is_prod else "/openapi.json",
)

app.mount("/assets", StaticFiles(directory="media/assets"), name="assets")
app.mount("/uploads", StaticFiles(directory="media/uploads"), name="uploads")

app.include_router(api_router)

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))
