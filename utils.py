import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_rdp(infile, outf):
    # Read and parse the JSON file
    try:
        with open(infile, "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading the JSON file: {e}")
        exit(1)

    # Look for the entry with internal port 3389
    internal_port_to_find = "3389"
    entry_found = None
    for entry in data: # need to parse str to json
        if entry.get("Internal Port") == internal_port_to_find:
            entry_found = entry
            break

    if entry_found:
        external_ip = entry_found.get("External IPv4 Address", "")
        external_port = entry_found.get("External Port", "")
        if external_ip and external_port:
            dynamic_ip = f"{external_ip}:{external_port}"
            logging.info(f"Found matching entry. Using {dynamic_ip} for RDP configuration.")

            # RDP settings template with dynamic IP
            rdp_template = {
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
                "full address": f"s:{dynamic_ip}",
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

            # Specify the output file path
            # outf = "dynamic_connection.rdp"

            # Write the RDP settings to the file
            with open(outf, "w") as file:
                for key, value in rdp_template.items():
                    file.write(f"{key}:{value}\n")

            logging.info(f"RDP file created: {outf}")
        else:
            logging.error("Could not find a valid external IP or port.")
    else:
        logging.warning(f"No entry with internal port {internal_port_to_find} was found.")
