from operator import or_
from models.res_config import ResConfig
from sqlmodel import Session, select, func

class ConfigMutations:
    def __init__(self, session: Session):
        self.db = session

    def create(self, new_config: ResConfig):

        config = self.db.add(new_config)
        self.db.commit()
        self.db.refresh()

        return config