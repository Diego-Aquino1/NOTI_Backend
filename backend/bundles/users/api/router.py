from fastapi import Request, APIRouter, Depends
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder
from backend.api.dependencies import get_db
from backend.bundles.users.controllers.get_all_users_controller import UserAllController
from backend.bundles.users.controllers.login_controller import LoginController
from backend.bundles.users.controllers.register_controller import RegisterController
from backend.bundles.users.schemas.auth_schemas import LoginRequest, RegisterRequest
# from backend.bundles.users.controllers.google_auth_controller import GoogleAuthController, GoogleAuthRequest # Nuevo controlador

from shared.utils.auth import BLACKLIST_TOKENS

router = APIRouter()

@router.get("/")
def test():
    return jsonable_encoder({"rpta", "Usuarios"})


#Registro de usuario
@router.post("/register", status_code = 201)
def register(data: RegisterRequest, session: Session = Depends(get_db)):
    controller = RegisterController(session)
    return jsonable_encoder(controller.run(data))

#Inicio de sesión
@router.post("/login", status_code = 200)
def login(data: LoginRequest, session: Session = Depends(get_db)):
    controller = LoginController(session)
    return jsonable_encoder(controller.run(data))

#Cierre de sesión
@router.post("/logout", status_code = 200)
def logout(token: str):
    BLACKLIST_TOKENS.add(token)
    return {"message": "Sesión cerrada correctamente"}

@router.get("/all", status_code = 200)
def get_roles(session: Session = Depends(get_db)):
    controller = UserAllController(session)
    return controller.run()

# 🔹 Nuevo: Inicio de sesión con Google
# @router.post("/auth/google", status_code=200)
# def google_login(data: GoogleAuthRequest):
#     controller = GoogleAuthController()
#     return jsonable_encoder(controller.run(data))