from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scraping.services.power_outage_scraper import PowerOutageScraper
import pytz
import asyncio

def start_scheduler():
    """Start the background scheduler for scraping tasks"""
    scheduler = BackgroundScheduler(timezone=pytz.timezone("America/Lima"))
    
    scraper = PowerOutageScraper()

    @scheduler.scheduled_job(
        CronTrigger(day_of_week='tue', hour=22, minute=4)  # Tuesdays at 22:04
    )
    def scheduled_scrape():
        print("⏳ Ejecutando scraping programado de cortes de luz...")
        asyncio.run(scraper.run_scraping())

    scheduler.start()
    print("🗓️ Scheduler iniciado...")

async def run_scraping():
    """Run scraping manually"""
    try:
        scraper = PowerOutageScraper()
        await scraper.run_scraping()
        print("✅ Scraping ejecutado correctamente")
    except Exception as e:
        print(f"❌ Error en el scraping: {e}")
