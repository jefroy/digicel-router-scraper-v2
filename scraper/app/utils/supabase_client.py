from typing import List, Dict
import httpx
import logging
from datetime import datetime
import socket
from app.models.port_forward import PortForward
from app.utils.config import settings

logger = logging.getLogger(__name__)

class SupabaseManager:
    def __init__(self):
        self.base_url = f"{settings.SUPABASE_URL}/rest/v1"
        self.headers = {
            "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"  # Get back the inserted/updated records
        }
        self.hostname = socket.gethostname()

    async def get_current_port_forwards(self, client: httpx.AsyncClient) -> List[Dict]:
        """Get current active port forwards for this host"""
        url = f"{self.base_url}/port_forwards"
        params = {
            "host_name": f"eq.{self.hostname}",
            "is_active": "eq.true",
            "select": "external_ipv4_address,external_port,internal_port,protocol,internal_ip"
        }

        response = await client.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []

    def has_changes(self, current: List[Dict], new_forwards: List[PortForward]) -> bool:
        """Check if there are any changes in the port forwards"""
        if len(current) != len(new_forwards):
            return True

        # Create sets of tuples for comparison
        current_set = {
            (
                pf['external_ipv4_address'],
                pf['external_port'],
                pf['internal_port'],
                pf['protocol'],
                pf['internal_ip']
            ) for pf in current
        }

        new_set = {
            (
                pf.external_ipv4_address,
                pf.external_port,
                pf.internal_port,
                pf.protocol,
                pf.internal_ip
            ) for pf in new_forwards
        }

        return current_set != new_set

    async def update_port_forwards(self, port_forwards: List[PortForward]) -> None:
        """Update port forwards in Supabase database only if there are changes"""
        try:
            async with httpx.AsyncClient() as client:
                # Get current port forwards
                current = await self.get_current_port_forwards(client)

                # Check if there are any changes
                if not self.has_changes(current, port_forwards):
                    logger.info("No changes detected in port forwards. Skipping update.")
                    return

                # If we have changes, proceed with update
                logger.info("Changes detected in port forwards. Updating database...")

                # First, mark all existing records for this host as inactive
                update_url = f"{self.base_url}/port_forwards"
                update_params = {
                    "host_name": f"eq.{self.hostname}"
                }
                await client.patch(
                    update_url,
                    headers=self.headers,
                    params=update_params,
                    json={"is_active": False}
                )

                logger.debug(f"Marked old records as inactive for host: {self.hostname}")

                # Convert port forwards to Supabase format
                records = []
                for pf in port_forwards:
                    # Set the hostname
                    pf.host_name = self.hostname
                    # Convert to Supabase format
                    records.append(pf.to_supabase())

                # Insert new records
                if records:
                    insert_url = f"{self.base_url}/port_forwards"
                    response = await client.post(
                        insert_url,
                        headers=self.headers,
                        json=records
                    )

                    if response.status_code in (200, 201, 204):
                        logger.info(f"Successfully updated {len(records)} port forwards in Supabase")
                    else:
                        logger.error(f"Error updating Supabase: {response.status_code} - {response.text}")
                else:
                    logger.warning("No port forwards to update")

        except Exception as e:
            logger.error(f"Error updating Supabase: {e}")
            raise