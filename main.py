from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importar routers
from routers.geo_location.api_geo_location import router as geo_location_router
from routers.res_users.api_res_users import router as user_router

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar esto a los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
