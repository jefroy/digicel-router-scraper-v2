from pathlib import Path
import logging
from typing import Dict, Any
from ..models.port_forward import PortForward

logger = logging.getLogger(__name__)

class RDPGenerator:
    def __init__(self):
        self.rdp_template = {
            "screen mode id": "i:2",
            "use multimon": "i:0",
            "desktopwidth": "i:2560",
            "desktopheight": "i:1440",
            "session bpp": "i:32",
            "winposstr": "s:0,1,385,86,1916,1269",
            "compression": "i:1",
            "keyboardhook": "i:2",
            "audiocapturemode": "i:1",
            "videoplaybackmode": "i:1",
            "connection type": "i:7",
            "networkautodetect": "i:1",
            "bandwidthautodetect": "i:1",
            "displayconnectionbar": "i:1",
            "enableworkspacereconnect": "i:0",
            "disable wallpaper": "i:0",
            "allow font smoothing": "i:0",
            "allow desktop composition": "i:0",
            "disable full window drag": "i:1",
            "disable menu anims": "i:1",
            "disable themes": "i:0",
            "disable cursor setting": "i:0",
            "bitmapcachepersistenable": "i:1",
            "audiomode": "i:0",
            "redirectprinters": "i:1",
            "redirectlocation": "i:0",
            "redirectcomports": "i:0",
            "redirectsmartcards": "i:1",
            "redirectclipboard": "i:1",
            "redirectposdevices": "i:0",
            "autoreconnection enabled": "i:1",
            "authentication level": "i:0",
            "prompt for credentials": "i:0",
            "negotiate security layer": "i:1",
            "remoteapplicationmode": "i:0",
            "alternate shell": "s:",
            "shell working directory": "s:",
            "gatewayhostname": "s:",
            "gatewayusagemethod": "i:4",
            "gatewaycredentialssource": "i:4",
            "gatewayprofileusagemethod": "i:0",
            "promptcredentialonce": "i:0",
            "gatewaybrokeringtype": "i:0",
            "use redirection server name": "i:0",
            "rdgiskdcproxy": "i:0",
            "kdcproxyname": "s:",
            "redirectwebauthn": "i:1",
            "enablerdsaadauth": "i:0",
            "drivestoredirect": "s:"
        }

    def generate_rdp_file(self, port_forward: PortForward, output_path: Path) -> bool:
        """
        Generate an RDP file for the given port forward configuration.
        
        Args:
            port_forward: PortForward object containing the connection details
            output_path: Path where the RDP file should be saved
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create a copy of the template and update the connection address
            rdp_config = self.rdp_template.copy()
            rdp_config["full address"] = f"s:{port_forward.connection_string}"

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the RDP file
            with open(output_path, "w") as f:
                for key, value in rdp_config.items():
                    f.write(f"{key}:{value}\n")

            logger.info(f"Generated RDP file at {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to generate RDP file: {e}")
            return False