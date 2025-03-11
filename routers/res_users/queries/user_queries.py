from operator import or_
from sqlmodel import Session, select, func

from models.res_users import ResUser

class UserQuery:
    def __init__(self, session: Session):
        self.db = session

    def find_all(self):
        query = select(ResUser)
        return self.db.exec(query).all()
    
    def find_by_email(self, email: str):
        query = select(ResUser).where(ResUser.email == email)
        return self.db.exec(query).first()