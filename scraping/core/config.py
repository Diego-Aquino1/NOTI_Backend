from shared.core.config import *

# Scraping specific configuration
SCRAPING_INTERVAL_MINUTES = int(os.getenv("SCRAPING_INTERVAL_MINUTES", "60"))
SCRAPING_ENABLED = os.getenv("SCRAPING_ENABLED", "True").lower() == "true"
