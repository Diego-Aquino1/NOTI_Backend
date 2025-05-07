from operator import or_
from models.res_config import ResConfig
from sqlmodel import Session, select, func


class ConfigQuery:
    def __init__(self, session: Session):
        self.db = session

    def find_all(self):
        query = select(ResConfig)
        return self.db.exec(query).all()
    
    def find_by_user(self, user_id: int):
        query = select(ResConfig).where(ResConfig.user_id == user_id)
        return self.db.exec(query).first()