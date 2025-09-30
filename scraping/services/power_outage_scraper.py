from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.connection import get_async_session
from ..shared.utils.estructura_data import obtener_cortes
import asyncio

class PowerOutageScraper:
    """Service for scraping power outage data"""
    
    def __init__(self):
        self.service_name = "PowerOutageScraper"
    
    async def run_scraping(self):
        """Run the scraping process"""
        try:
            print("⏳ Iniciando scraping de cortes de luz...")
            
            async for session in get_async_session():
                await obtener_cortes(session)
                print("✅ Scraping completado correctamente")
                break
                
        except Exception as e:
            print(f"❌ Error en el scraping: {e}")
            raise e
    
    async def get_scraping_status(self):
        """Get current scraping status"""
        return {
            "service": self.service_name,
            "status": "running",
            "last_run": "N/A"  # TODO: Implement last run tracking
        }
