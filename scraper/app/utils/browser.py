from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from contextlib import contextmanager
import logging

from app.utils.config import settings

logger = logging.getLogger(__name__)

class BrowserManager:
    @staticmethod
    def setup_chrome_options() -> Options:
        options = Options()
        for option in settings.CHROME_OPTIONS:
            options.add_argument(option)
        options.add_argument(f'user-agent={settings.USER_AGENT}')
        return options

    @contextmanager
    def get_browser(self):
        driver = None
        try:
            driver = webdriver.Chrome(options=self.setup_chrome_options())
            yield driver
        except Exception as e:
            logger.error(f"Browser error: {e}")
            raise
        finally:
            if driver:
                driver.quit()

    def login_to_router(self, driver: webdriver.Chrome) -> bool:
        """Login to router with configured credentials"""
        try:
            logger.info("Attempting to log in to router...")
            driver.get(settings.ROUTER_URL)

            # Wait for login form
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txt_Username"))
            )

            # Enter credentials
            driver.find_element(By.ID, "txt_Username").send_keys(settings.ROUTER_USERNAME)
            driver.find_element(By.ID, "txt_Password").send_keys(settings.ROUTER_PASSWORD)
            driver.find_element(By.ID, "button").click()

            # Wait for login to complete
            driver.implicitly_wait(10)

            logger.info("Successfully logged in to router")
            return True

        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False