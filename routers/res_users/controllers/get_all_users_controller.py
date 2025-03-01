from datetime import datetime
from database import get_session
from routers.res_users.queries.user_queries import UserQuery
# from utilities.auth import ApiAuth

class UserAllController:
    def __init__(self) -> None:
        session = get_session()
        self.query = UserQuery(session)

    # def run(self, auth: ApiAuth):
    def run(self):

        users = self.query.find_all()

        return users