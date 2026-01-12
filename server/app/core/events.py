from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base

def create_start_app_handler(app: FastAPI):
    async def start_app() -> None:
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.create_all)
        print("🚀 Application started")
    return start_app


def create_stop_app_handler(app: FastAPI):
    async def stop_app() -> None:
        # Close DB connections
        await engine.dispose()
        print("🛑 Application stopped")
    return stop_app