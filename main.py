from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

from routers.geo_location import api_geo_location
from routers.res_users import api_res_users
from fastapi import FastAPI, HTTPException, Depends
from google.auth.transport import requests
from google.oauth2 import id_token
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Cargar variables de entorno
load_dotenv()

# Obtener CLIENT_ID de Google desde .env
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

app = FastAPI()

app.include_router(api_res_users.router)
app.include_router(api_geo_location.router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
async def testing():
    return {"hola": "Si corre"}

# Definir esquema para la petición de autenticación
class GoogleAuthRequest(BaseModel):
    id_token: str

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/google")
def google_login(auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
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

        # Verificar si el usuario ya existe en la BD
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

        return {"message": "Login exitoso", "user": user.email}

    except ValueError:
        raise HTTPException(status_code=400, detail="Token inválido")