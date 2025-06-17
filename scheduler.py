from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scraping.utilities.estructura_data import obtener_cortes
from scraping.database import get_session
import pytz
import asyncio

def start_scheduler():
    scheduler = BackgroundScheduler(timezone = pytz.timezone("America/Lima"))

    @scheduler.scheduled_job(
        CronTrigger(day_of_week='tue', hour=22, minute=4)  # Sábados = sat; mon, tue, wed, thu, fri, sat, sun
    )
    def scheduled_scrape():
        print("⏳ Ejecutando scraping programado de cortes de luz...")
        asyncio.run(run_scraping())

    scheduler.start()
    print("🗓️ Scheduler iniciado...")

async def run_scraping():
    try:
        async for session in get_session():
            await obtener_cortes(session)
            print("✅ Scraping programado ejecutado correctamente")
            break
    except Exception as e:
        print(f"❌ Error en el scraping programado: {e}")
