import time

# All your imports and other setup code remains the same
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from bs4 import BeautifulSoup
import json
import socket
import pandas as pd
import os
from dotenv import load_dotenv

from utils import generate_rdp

# Load environment variables
load_dotenv()

# Retrieve environment variables
dump_path = os.getenv('DUMP_PATH')

# Logging setup
logging.basicConfig(filename='selenium_errors.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# URLs and paths
target_url = "http://192.168.100.1/html/bbsp/pcp/pcp.asp"
hostname = socket.gethostname()
target_dump_path = f"{dump_path}\\{hostname}-ports\\"

# Configure ChromeOptions to run headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920x1080")

executable_path = "path_to_chromedriver"  # Update to your Chromedriver's path

# Main loop
while True:
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)
    print(driver.title)  # Confirm page load

    try:
        print("on login page..")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txt_Username")))
        driver.find_element(By.ID, "txt_Username").send_keys("Digicel")
        driver.find_element(By.ID, "txt_Password").send_keys("Digicel")
        print("entered creds.. trying to login..")
        driver.find_element(By.ID, "button").click()
        driver.implicitly_wait(10)
        print("logged in!")

        print("attempting to go to pcp page...")
        driver.get(target_url)
        driver.implicitly_wait(10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', id='PcpConfigList')
        filtered_data = []
        headers = [header.text.strip() for header in table.find('tr', class_='head_title').find_all('td')]

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            row_data = {}
            if cols[1].text.strip() == "Manual":
                for idx, col in enumerate(cols):
                    header = headers[idx]
                    if header:
                        row_data[header] = col.text.strip()
                filtered_data.append(row_data)

        json_data = json.dumps(filtered_data, indent=4)
        print(json_data)
        json_data = json.loads(json_data)

        filename = target_dump_path + f"ports"
        if not os.path.exists(target_dump_path):
            os.makedirs(target_dump_path)
            print(f"Directory created at {target_dump_path}")
        else:
            print(f"Directory already exists at {target_dump_path}")

        with open(filename + ".json", 'w') as json_file:
            json.dump(json_data, json_file)

        df = pd.DataFrame(filtered_data)
        csv_file_path = filename + ".csv"
        df.to_csv(csv_file_path, index=False)

        generate_rdp(f"{filename}.json", f"{target_dump_path}{hostname}.rdp")

    except Exception as e:
        logging.error("An error occurred: %s", e)

    finally:
        driver.quit()

    # Countdown for 5 minutes
    for i in range(300, 0, -1):
        time.sleep(1)
        print(f'Next iteration in {i} seconds.', end='\r')
