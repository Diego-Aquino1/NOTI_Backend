from fastapi import HTTPException
from sqlmodel import Session
from backend.bundles.profiles.queries.profile_queries import ProfileQuery
from backend.bundles.users.queries.user_queries import UserQuery
from backend.bundles.users.schemas.auth_schemas import LoginRequest
from shared.utils.auth import create_jwt, verify_password

class LoginController:
    def __init__(self, session: Session) -> None:
        self.session = session
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