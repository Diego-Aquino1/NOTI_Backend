from operator import or_
from sqlmodel import Session, select

from models.res_profiles import ResProfile

class ProfileQuery:
    def __init__(self, session: Session):
        self.db = session
    
    def find_by_user_id(self, user_id: int):
        query = select(ResProfile).where(ResProfile.user_id == user_id)
        return self.db.exec(query).first()