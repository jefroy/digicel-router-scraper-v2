from bs4 import BeautifulSoup
import pandas as pd
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from selenium import webdriver

from app.models.port_forward import PortForward
from app.utils.config import settings

logger = logging.getLogger(__name__)

class PortForwardScraper:
    def parse_table(self, page_source: str) -> List[PortForward]:
        """Parse the port forwarding table and return a list of PortForward objects"""
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', id='PcpConfigList')
        if not table:
            logger.error("Could not find port forwarding table")
            return []

        headers = [header.text.strip() for header in table.find('tr', class_='head_title').find_all('td')]
        port_forwards = []

        for row in table.find_all('tr')[1:]:  # Skip header row
            cols = row.find_all('td')
            if cols[1].text.strip() == "Manual":  # Only process manual entries
                row_data = {
                    headers[i]: col.text.strip()
                    for i, col in enumerate(cols)
                    if headers[i]  # Only process if header exists
                }
                try:
                    port_forward = PortForward.parse_obj(row_data)
                    port_forwards.append(port_forward)
                except Exception as e:
                    logger.error(f"Error parsing row: {e}")

        return port_forwards

    def save_data(self, port_forwards: List[PortForward]) -> None:
        """Save port forwards to JSON and CSV files"""
        # Ensure output directory exists
        settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Convert to list of dictionaries for saving
        data = [pf.dict(by_alias=True) for pf in port_forwards]

        # Save JSON
        json_path = settings.OUTPUT_DIR / "ports.json"
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved JSON to {json_path}")

        # Save CSV
        csv_path = settings.OUTPUT_DIR / "ports.csv"
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved CSV to {csv_path}")

    async def scrape(self, driver: webdriver.Chrome) -> List[PortForward]:
        """Main scraping function"""
        try:
            # Navigate to port forwarding page
            driver.get(settings.ROUTER_URL)
            driver.implicitly_wait(10)

            # Parse and save data
            port_forwards = self.parse_table(driver.page_source)
            if port_forwards:
                self.save_data(port_forwards)

            return port_forwards

        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return []