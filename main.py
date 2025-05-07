from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importar routers
from routers.geo_location.api_geo_location import router as geo_location_router
from routers.res_users.api_res_users import router as user_router

# Crear la aplicación FastAPI
from database import get_session
from contextlib import asynccontextmanager
from utilities.estructura_data import obtener_cortes  # Reemplaza esto con la ruta real donde está tu función
import asyncio

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
app.include_router(user_router, prefix="/api/user")  
app.include_router(geo_location_router, prefix="/api/geo")  

# Ruta principal
@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

# Ruta de prueba
@app.get("/test")
async def testing():
    return {"hola": "Si corre"}

# Ejecutar el servidor solo si este archivo es el punto de entrada
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    
# Web scraping y guardado en PostgreSQL al iniciar el servidor
@app.on_event("startup")
async def startup_event():
    async for session in get_session():
        try:
            await obtener_cortes(session)
            print("✅ Web scraping completado y datos almacenados.")
        except Exception as e:
            print(f"❌ Error durante web scraping al iniciar: {e}")
