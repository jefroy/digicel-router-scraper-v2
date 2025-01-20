import asyncio
import logging
from pathlib import Path
import time

from utils.config import settings
from utils.browser import BrowserManager
from utils.scraper import PortForwardScraper
from utils.rdp import RDPGenerator

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path("logs/app.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    browser_manager = BrowserManager()
    scraper = PortForwardScraper()
    rdp_generator = RDPGenerator()

    while True:
        try:
            with browser_manager.get_browser() as driver:
                if browser_manager.login_to_router(driver):
                    # Scrape port forwards
                    port_forwards = await scraper.scrape(driver)

                    # Generate RDP file for any RDP port forwards
                    rdp_port_forwards = [pf for pf in port_forwards if pf.is_rdp]
                    if rdp_port_forwards:
                        rdp_generator.generate_rdp_file(
                            rdp_port_forwards[0],
                            settings.OUTPUT_DIR / f"{settings.HOSTNAME}.rdp"
                        )

                    logger.info(f"Completed iteration, waiting {settings.REFRESH_INTERVAL} seconds")
                else:
                    logger.error("Failed to log in to router")

        except Exception as e:
            logger.error(f"Error in main loop: {e}")

        finally:
            # Wait for next iteration
            await asyncio.sleep(settings.REFRESH_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())