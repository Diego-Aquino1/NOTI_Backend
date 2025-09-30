from datetime import datetime
from sqlmodel import Session
from backend.bundles.users.queries.user_queries import UserQuery
# from shared.utils.auth import ApiAuth

class UserAllController:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.query = UserQuery(session)

    # def run(self, auth: ApiAuth):
    def run(self):
        users = self.query.find_all()
        return users