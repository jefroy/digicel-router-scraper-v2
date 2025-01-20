import asyncio
import logging
from pathlib import Path

from app.utils.config import settings
from app.utils.browser import BrowserManager
from app.utils.scraper import PortForwardScraper
from app.utils.rdp import RDPGenerator

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to console only for testing
    ]
)

logger = logging.getLogger(__name__)

async def test_run():
    browser_manager = BrowserManager()
    scraper = PortForwardScraper()
    rdp_generator = RDPGenerator()

    try:
        with browser_manager.get_browser() as driver:
            if browser_manager.login_to_router(driver):
                logger.info("Successfully logged in")

                # Scrape port forwards
                port_forwards = await scraper.scrape(driver)
                logger.info(f"Found {len(port_forwards)} port forwards")

                # Generate RDP file for any RDP port forwards
                rdp_port_forwards = [pf for pf in port_forwards if pf.is_rdp]
                if rdp_port_forwards:
                    logger.info(f"Found {len(rdp_port_forwards)} RDP port forwards")
                    rdp_generator.generate_rdp_file(
                        rdp_port_forwards[0],
                        settings.OUTPUT_DIR / f"{settings.HOSTNAME}.rdp"
                    )
                else:
                    logger.info("No RDP port forwards found")
            else:
                logger.error("Failed to log in to router")

    except Exception as e:
        logger.error(f"Error in test run: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_run())