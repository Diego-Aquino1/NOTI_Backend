from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from passlib.context import CryptContext

from utilities.env import ALGORITHM, SECRET_KEY


# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

BLACKLIST_TOKENS = set()

# Función para hashear contraseña
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para generar JWT
def create_jwt(email: str, name: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "name": name, "exp": expiration}
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