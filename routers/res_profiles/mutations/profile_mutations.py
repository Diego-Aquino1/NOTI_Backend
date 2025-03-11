from operator import or_
from sqlmodel import Session

from models.res_profiles import ResProfile

class ProfileMutations:
    def __init__(self, session: Session):
        self.db = session

    def create(self, new_profile: ResProfile):

        user = self.db.add(new_profile)
        #session.commit()
        self.db.flush()

        return user