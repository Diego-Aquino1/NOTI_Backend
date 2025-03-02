from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import datetime
from database import get_session  # Importa la sesión de base de datos
from routers.res_users.queries.user_queries import UserQuery
from models.res_users import ResUser  # Modelo de usuario

router = APIRouter()

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta para JWT
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# Lista negra de tokens (para logout)
BLACKLIST_TOKENS = set()

# Modelos de datos
class RegisterRequest(BaseModel):
    email: str
    pwd: str

class LoginRequest(BaseModel):
    email: str
    pwd: str

# Función para hashear contraseña
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para generar JWT
def create_jwt(email: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"sub": email, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Función para decodificar JWT
def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Retorna email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

#Registro de usuario
@router.post("/register")
def register(data: RegisterRequest):
    session = get_session()
    query = UserQuery(session)

    # Verificar si el usuario ya existe
    existing_user = query.find_by_email(data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    # Crear nuevo usuario
    new_user = ResUser(email=data.email, password=hash_password(data.pwd))
    session.add(new_user)
    session.commit()

    return {"message": "Usuario registrado exitosamente"}

#Inicio de sesión
@router.post("/login")
def login(data: LoginRequest):
    session = get_session()
    query = UserQuery(session)

    # Buscar usuario en la base de datos
    user = query.find_by_email(data.email)
    if not user or not verify_password(data.pwd, user.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    # Crear JWT
    token = create_jwt(data.email)
    return {"email": data.email, "jwt": token, "data": "Logeado correctamente"}

#Cierre de sesión
@router.post("/logout")
def logout(token: str):
    BLACKLIST_TOKENS.add(token)  # Agregar token a lista negra
    return {"message": "Sesión cerrada correctamente"}