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

# Set up logging
logging.basicConfig(filename='selenium_errors.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

target_url = "http://192.168.100.1/html/bbsp/pcp/pcp.asp"

hostname = socket.gethostname()
target_dump_path = f"C:\\Users\\idisc\\OneDrive\\Documents\\APPS\\{hostname}-ports\\"

# Configure ChromeOptions to run headless
options = Options()
options.add_argument("--headless")  # Ensures Chrome runs in headless mode
options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--window-size=1920x1080")  # Optional: Set window size

# Ensure the path to chromedriver is set if not included in PATH
executable_path = "path_to_chromedriver"  # Update this to your Chromedriver's path

# Instantiate a webdriver with the options
driver = webdriver.Chrome(options=options)

# Example of navigating to a page and printing its title in headless mode
driver.get(target_url)
print(driver.title)  # Output the title of the page to verify it loaded correctly

try:
    # Example of interacting with the page
    # Suppose you need to login first
    print("on login page..")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txt_Username")))
    driver.find_element(By.ID, "txt_Username").send_keys("Digicel")
    driver.find_element(By.ID, "txt_Password").send_keys("Digicel")
    print("entered creds.. trying to login..")
    driver.find_element(By.ID, "button").click()

    # Wait for the login to complete and check if we are logged in
    driver.implicitly_wait(10)
    print("logged in!")

    # Navigate to another page or perform further actions
    print("attempting to go to pcp page...")
    driver.get(target_url)
    driver.implicitly_wait(10)
    # print(driver.title)  # Output the title of the page to verify it loaded correctly
    # print(driver.page_source)  # Output the title of the page to verify it loaded correctly
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table by ID
    table = soup.find('table', id='PcpConfigList')

    # Initialize a list to store each row's data
    filtered_data = []

    # Headers
    headers = [header.text.strip() for header in table.find('tr', class_='head_title').find_all('td')]

    # Iterate over each row in the table, starting from the second row (first row is headers)
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cols = row.find_all('td')
        row_data = {}
        if cols[1].text.strip() == "Manual":  # Check if the Configuration Mode is "Manual"
            for idx, col in enumerate(cols):
                header = headers[idx]
                if header:  # Only add data if the header is not empty
                    row_data[header] = col.text.strip()
            filtered_data.append(row_data)

    # Convert the filtered entries to JSON
    json_data = json.dumps(filtered_data, indent=4)
    print(json_data)

    filename = target_dump_path + f"ports"

    # Check if the directory exists, and if not, create it
    if not os.path.exists(target_dump_path):
        os.makedirs(target_dump_path)
        print(f"Directory created at {target_dump_path}")
    else:
        print(f"Directory already exists at {target_dump_path}")

    with open(filename + ".json", 'w') as json_file:
        json.dump(json_data, json_file)

    # Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(filtered_data)

    # Define the CSV file path
    csv_file_path = filename + ".csv"

    # Writing data to CSV
    df.to_csv(csv_file_path, index=False)


except Exception as e:
    logging.error("An error occurred: %s", e)

finally:
    # When you're done, close the driver
    driver.quit()
