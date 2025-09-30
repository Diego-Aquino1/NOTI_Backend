from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraping.core.config import SCRAPING_HOST, SCRAPING_PORT
from scraping.services.power_outage_scraper import PowerOutageScraper

def create_scraping_app() -> FastAPI:
    """Create and configure FastAPI application for scraping service"""
    app = FastAPI(
        title="NOTI Scraping Service",
        description="Scraping service for NOTI - Power Outage Notification System",
        version="1.0.0"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def health_check():
        return {"status": "healthy", "service": "scraping"}

    @app.post("/trigger")
    async def trigger_scraping():
        """Trigger scraping manually"""
        try:
            scraper = PowerOutageScraper()
            await scraper.run_scraping()
            return {"status": "✅ Scraping ejecutado correctamente"}
        except Exception as e:
            return {"status": "❌ Error durante scraping", "detail": str(e)}

    @app.on_event("startup")
    async def startup_scraping():
        """Run scraping on startup"""
        try:
            scraper = PowerOutageScraper()
            await scraper.run_scraping()
            print("✅ Scraping automático al iniciar completado")
        except Exception as e:
            print(f"❌ Error en scraping al iniciar: {e}")

    return app

# Create the app instance
app = create_scraping_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SCRAPING_HOST, port=SCRAPING_PORT)
