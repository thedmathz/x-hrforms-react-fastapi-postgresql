from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Use pool sizing for production
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # disable verbose SQL logging in prod
    pool_size=20,  # adjust based on expected concurrent DB connections
    max_overflow=10,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncSession:
    """
    FastAPI dependency for a session per request.
    Service layer should manage transactions with async with db.begin().
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
