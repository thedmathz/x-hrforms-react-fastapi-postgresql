from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base

def create_start_app_handler(app: FastAPI):
    async def start_app() -> None:
        # Initialize database tables
        Base.metadata.create_all(bind=engine)
        # Example: connect to Redis, RabbitMQ, etc.
        # await redis.connect()
        print("🚀 Application started")
    return start_app


def create_stop_app_handler(app: FastAPI):
    async def stop_app() -> None:
        # Close DB connections
        await engine.dispose()
        print("🛑 Application stopped")
    return stop_app