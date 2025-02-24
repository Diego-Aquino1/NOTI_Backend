from sqlmodel import Session, create_engine
from utilities.env import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
print(f'Connecting to {url}')
engine = create_engine(url)

def getEngine():
    return engine

def get_session():
    with Session(engine) as session:
        return session
