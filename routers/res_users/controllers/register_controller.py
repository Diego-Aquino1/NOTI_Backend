from fastapi import HTTPException
from database import get_session
from models.res_profiles import ResProfile
from models.res_users import ResUser
from routers.res_profiles.mutations.profile_mutations import ProfileMutations
from routers.res_users.mutations.user_mutations import UserMutations
from routers.res_users.queries.user_queries import UserQuery
from routers.res_users.schemas.auth_schemas import RegisterRequest
from utilities.auth import hash_password

class RegisterController:
    def __init__(self) -> None:
        session = get_session()
        self.query = UserQuery(session)
        self.user_mutation = UserMutations(session)
        self.profile_mutation = ProfileMutations(session)

    def run(self, data: RegisterRequest):

        existing_user = self.query.find_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code = 400, detail="Usuario ya registrado")

        new_user = ResUser(email = data.email, pwd_hash = hash_password(data.pwd))

        self.user_mutation.create(new_user=new_user)

        new_profile = ResProfile(
            user_id = new_user.id, 
            name = data.name,  
            phone = data.phone,
            address = data.address,
            city = data.city,
            country = data.country,
        )
        
        self.profile_mutation.create(new_profile=new_profile)

        return {"message": "Usuario registrado exitosamente"}