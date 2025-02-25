# app/main_test.py
import asyncio
import logging
from pathlib import Path

from app.utils.config import settings
from app.utils.browser import BrowserManager
from app.utils.scraper import PortForwardScraper

# Setup logging - test version only logs to console
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Test version - runs only once instead of continuously"""
    browser_manager = BrowserManager()
    scraper = PortForwardScraper()

    try:
        with browser_manager.get_browser() as driver:
            if browser_manager.login_to_router(driver):
                logger.info("Successfully logged in")

                # Scrape port forwards
                port_forwards = await scraper.scrape(driver)
                logger.info(f"Found {len(port_forwards)} port forwards")

                # Log RDP forwards specifically
                rdp_forwards = [pf for pf in port_forwards if pf.is_rdp]
                if rdp_forwards:
                    logger.info(f"Found {len(rdp_forwards)} RDP port forwards")
                else:
                    logger.info("No RDP port forwards found")
            else:
                logger.error("Failed to log in to router")

    except Exception as e:
        logger.error(f"Error in test run: {e}")
        raise

if __name__ == "__main__":
    # Run once for testing
    asyncio.run(main())
