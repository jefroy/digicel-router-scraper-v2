from bs4 import BeautifulSoup
import pandas as pd
import json
import logging
from pathlib import Path
from typing import List
from selenium import webdriver

from app.models.port_forward import PortForward
from app.utils.supabase_client import SupabaseManager
from app.utils.config import settings
from app.utils.rdp import generate_rdp

logger = logging.getLogger(__name__)

class PortForwardScraper:
    def __init__(self):
        self.supabase = SupabaseManager()

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
            if len(cols) >= len(headers):  # Ensure we have enough columns
                row_data = {}
                for i, col in enumerate(cols):
                    if i < len(headers) and headers[i]:  # Only process if header exists
                        row_data[headers[i]] = col.text.strip()

                if row_data.get("Configuration Mode") == "Manual":  # Only process manual entries
                    try:
                        port_forward = PortForward.parse_obj(row_data)
                        port_forwards.append(port_forward)
                        logger.debug(f"Successfully parsed port forward: {port_forward}")
                    except Exception as e:
                        logger.error(f"Error parsing row: {e}")
                        logger.debug(f"Row data: {row_data}")

        return port_forwards

    def save_to_files(self, port_forwards: List[PortForward]) -> None:
        """Save port forwards to JSON and CSV files"""
        try:
            # Ensure output directory exists
            output_dir = Path(settings.DUMP_PATH) / f"{settings.HOSTNAME}-ports"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Convert to list of dictionaries for saving
            data = [pf.dict(by_alias=True) for pf in port_forwards]

            # Save JSON
            json_path = output_dir / "ports.json"
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Saved JSON to {json_path}")

            # Save CSV
            csv_path = output_dir / "ports.csv"
            df = pd.DataFrame(data)
            df.to_csv(csv_path, index=False)
            logger.info(f"Saved CSV to {csv_path}")

            # Generate RDP file if needed
            rdp_ports = [pf for pf in port_forwards if pf.is_rdp]
            if rdp_ports:
                rdp_path = output_dir / f"{settings.HOSTNAME}.rdp"
                generate_rdp(rdp_ports[0], rdp_path)
                logger.info(f"Generated RDP file at {rdp_path}")

        except Exception as e:
            logger.error(f"Error saving files: {e}")
            raise

    async def scrape(self, driver: webdriver.Chrome) -> List[PortForward]:
        """Main scraping function"""
        try:
            # Navigate to port forwarding page
            driver.get(settings.ROUTER_URL)
            driver.implicitly_wait(10)

            # Parse data
            port_forwards = self.parse_table(driver.page_source)
            logger.debug(f"Found {len(port_forwards)} port forwards")

            if port_forwards:
                # Save to files
                if settings.ENABLE_FILE_DUMP:
                    self.save_to_files(port_forwards)

                # Update Supabase
                await self.supabase.update_port_forwards(port_forwards)
                logger.info(f"Successfully processed {len(port_forwards)} port forwards")
            else:
                logger.warning("No port forwards found")

            return port_forwards

        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return []