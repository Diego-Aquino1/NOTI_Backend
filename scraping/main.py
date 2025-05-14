from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from utilities.estructura_data import obtener_cortes # type: ignore

app = FastAPI()

# CORS settings (ajusta si necesitas restringir orígenes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Scraper API funcionando"}

@app.post("/trigger")
async def trigger_scraping(session: AsyncSession = Depends(get_session)):
    try:
        await obtener_cortes(session)
        return {"status": "✅ Scraping ejecutado correctamente"}
    except Exception as e:
        return {"status": "❌ Error durante scraping", "detail": str(e)}

@app.on_event("startup")
async def startup_scraping():
    try:
        async for session in get_session():
            await obtener_cortes(session)
            print("✅ Scraping automático al iniciar completado")
            break
    except Exception as e:
        print(f"❌ Error en scraping al iniciar: {e}")