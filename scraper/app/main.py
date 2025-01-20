import asyncio
import logging
from pathlib import Path
import time
import os

from app.utils.config import settings
from app.utils.browser import BrowserManager
from app.utils.scraper import PortForwardScraper

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "app.log"

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    browser_manager = BrowserManager()
    scraper = PortForwardScraper()

    while True:
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
            logger.error(f"Error in main loop: {e}")

        finally:
            # Wait for next iteration
            logger.info(f"Waiting {settings.REFRESH_INTERVAL} seconds before next check")
            await asyncio.sleep(settings.REFRESH_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise