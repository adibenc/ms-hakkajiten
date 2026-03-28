"""SQLAlchemy database session management following fa-pidum pattern"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import config

# Base for SQLAlchemy models
Base = declarative_base()

# Connection URLs
DB_URL_SYNC = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
DB_URL_ASYNC = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

# Synchronous Engine (for Alembic migrations)
sync_engine = create_engine(
    DB_URL_SYNC,
    pool_pre_ping=True,
    echo=config.DEBUG
)

# Asynchronous Engine (for FastAPI)
async_engine = create_async_engine(
    DB_URL_ASYNC,
    pool_pre_ping=True,
    echo=config.DEBUG
)

# Session Factories
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Dependency for FastAPI routes
async def get_db():
    """Database session dependency for FastAPI"""
    async with AsyncSessionLocal() as session:
        yield session


# Synchronous session for non-async contexts
def get_sync_db():
    """Synchronous database session"""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
