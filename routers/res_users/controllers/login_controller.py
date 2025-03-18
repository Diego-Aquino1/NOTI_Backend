from fastapi import HTTPException
from database import get_session
from routers.res_profiles.queries.profile_queries import ProfileQuery
from routers.res_users.queries.user_queries import UserQuery
from routers.res_users.schemas.auth_schemas import LoginRequest
from utilities.auth import create_jwt, verify_password

class LoginController:
    def __init__(self) -> None:
        session = get_session()
        self.user_query = UserQuery(session)
        self.profile_query = ProfileQuery(session)

    def run(self, data: LoginRequest):

        # Buscar usuario en la base de datos
        user = self.user_query.find_by_email(data.email)
        if not user or not verify_password(data.pwd, user.pwd_hash):
            raise HTTPException(status_code = 401, detail="Credenciales incorrectas")
        
        name = self.profile_query.find_by_user_id(user_id = user.id).name
        
        token = create_jwt(data.email, name)

        return {"email": data.email, "name": name, "jwt": token, "response": "Logeado correctamente"}