from sqlmodel import Session, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..core.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

# Synchronous database URL
SYNC_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
# Asynchronous database URL
ASYNC_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# Synchronous engine
sync_engine = create_engine(SYNC_DATABASE_URL)
# Asynchronous engine
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

def get_sync_engine():
    """Get synchronous database engine"""
    return sync_engine

def get_async_engine():
    """Get asynchronous database engine"""
    return async_engine

def get_sync_session():
    """Get synchronous database session"""
    with Session(sync_engine) as session:
        return session

def get_session():
    """Alias for get_sync_session for backward compatibility"""
    return get_sync_session()

async def get_async_session():
    """Get asynchronous database session"""
    async with async_session() as session:
        yield session
