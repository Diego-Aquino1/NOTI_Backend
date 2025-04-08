from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

from routers.geo_location import api_geo_location
from routers.res_users import api_res_users

from database import get_session
from contextlib import asynccontextmanager
from utilities.estructura_data import obtener_cortes  # Reemplaza esto con la ruta real donde está tu función
import asyncio

app = FastAPI()

app.include_router(api_res_users.router)
app.include_router(api_geo_location.router)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
async def testing():
    return {"hola": "Si corre"}

# Web scraping y guardado en PostgreSQL al iniciar el servidor
@app.on_event("startup")
async def startup_event():
    async for session in get_session():
        try:
            await obtener_cortes(session)
            print("✅ Web scraping completado y datos almacenados.")
        except Exception as e:
            print(f"❌ Error durante web scraping al iniciar: {e}")