from fastapi import Request, APIRouter
from fastapi.encoders import jsonable_encoder
from routers.res_users.controllers.get_all_users_controller import UserAllController
from routers.res_users.controllers.login_controller import LoginController
from routers.res_users.controllers.register_controller import RegisterController
from routers.res_users.schemas.auth_schemas import LoginRequest, RegisterRequest
from routers.res_users.controllers.google_auth_controller import GoogleAuthController, GoogleAuthRequest # Nuevo controlador

from utilities.auth import BLACKLIST_TOKENS

router = APIRouter(prefix="/user")

@router.get("/")
def test():
    return jsonable_encoder({"rpta", "Usuarios"})


#Registro de usuario
@router.post("/register", status_code = 201)
def register(data: RegisterRequest):
    controller = RegisterController()
    return jsonable_encoder(controller.run(data))

#Inicio de sesión
@router.post("/login", status_code = 200)
def login(data: LoginRequest):
    controller = LoginController()
    return jsonable_encoder(controller.run(data))

#Cierre de sesión
@router.post("/logout", status_code = 200)
def logout(token: str):
    BLACKLIST_TOKENS.add(token)
    return {"message": "Sesión cerrada correctamente"}


@router.get("/all", status_code = 200)
# def get_roles(auth = Auth()):
def get_roles():
    controller = UserAllController()
    # return jsonable_encoder(controller.run(auth))
    #return jsonable_encoder(controller.run())
    return controller.run()

# 🔹 Nuevo: Inicio de sesión con Google
@router.post("/auth/google", status_code=200)
def google_login(data: GoogleAuthRequest):
    controller = GoogleAuthController()
    return jsonable_encoder(controller.run(data))