from fastapi import APIRouter, HTTPException, Depends
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import jwt  # Para generar el token JWT
from dotenv import load_dotenv
from models.res_users import ResUser as User  

from database import SessionLocal

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta")  # Para firmar el JWT

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    id_token: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GoogleAuthController:
    def run(self, auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
        try:
            # Verificar el token de Google
            idinfo = id_token.verify_oauth2_token(
                auth_data.id_token, requests.Request(), GOOGLE_CLIENT_ID
            )

            if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                raise HTTPException(status_code=400, detail="Emisor no válido")

            google_id = idinfo["sub"]
            email = idinfo["email"]
            name = idinfo.get("name", "")

            # Verificar si el usuario ya existe en la base de datos
            user = db.query(User).filter(User.google_id == google_id).first()
            if not user:
                new_user = User(
                    google_id=google_id,
                    email=email,
                    name=name,
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user = new_user

            # Generar un token JWT
            token_payload = {"sub": user.id, "email": user.email}
            jwt_token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

            return {
                "message": "Login exitoso",
                "user": {"email": user.email, "name": user.name},
                "jwt": jwt_token
            }

        except ValueError:
            raise HTTPException(status_code=400, detail="Token inválido")

# Registrar el endpoint en FastAPI
@router.post("/auth/google")
async def google_login(auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    return GoogleAuthController().run(auth_data, db)
