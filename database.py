from sqlmodel import Session, create_engine
from utilities.env import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

#url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

print(f'Connecting to {url}')

#engine = create_engine(url)
engine = create_async_engine(url, echo = True)  
async_session = sessionmaker(engine, class_ = AsyncSession, expire_on_commit = False)

def getEngine():
    return engine

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
