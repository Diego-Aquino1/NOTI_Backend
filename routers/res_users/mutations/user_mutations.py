from operator import or_
from sqlmodel import Session, select, func

from models.res_users import ResUser

class UserMutations:
    def __init__(self, session: Session):
        self.db = session

    def create(self, new_user: ResUser):

        user = self.db.add(new_user)
        #session.commit()
        self.db.commit()

        return user