from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import pytz
import asyncio

# Importar routers
from routers.geo_location.api_geo_location import router as geo_location_router
from routers.res_users.api_res_users import router as user_router
from scheduler import start_scheduler, run_scraping

from database import get_session

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins= origins,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"],
)

# Registrar routers con prefijos para organizar las rutas
app.include_router(user_router)  
app.include_router(geo_location_router)  

# Ruta principal
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

# Ruta de prueba
@app.get("/test")
async def testing():
    return {"hola": "Si corre"}

@app.on_event("startup")
async def startup_event():
    print("🚀 Iniciando servidor FastAPI...")
    start_scheduler()

    # Verifica si hoy es sábado a las 21:00 en Lima
    lima_now = datetime.now(pytz.timezone("America/Lima"))
    if lima_now.weekday() == 1 and lima_now.hour == 22 and lima_now.minute == 4:  # 0 = lunes,  5 =  sabado
        print("📅 Es sábado 21:00, ejecutando scraping ahora...")
        await run_scraping()

# Ejecutar el servidor solo si este archivo es el punto de entrada
if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
