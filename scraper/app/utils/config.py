from pydantic_settings import BaseSettings
from typing import List
import socket
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file explicitly
load_dotenv()

class Settings(BaseSettings):
    # Router settings
    ROUTER_URL: str = "http://192.168.100.1/html/bbsp/pcp/pcp.asp"
    ROUTER_USERNAME: str = "Digicel"
    ROUTER_PASSWORD: str = "Digicel"

    # Application settings
    DUMP_PATH: str = "./data"
    LOG_LEVEL: str = "INFO"
    REFRESH_INTERVAL: int = 300
    ENABLE_FILE_DUMP: bool = True
    HOSTNAME: str = socket.gethostname()

    # Chrome settings
    CHROME_WINDOW_SIZE: str = "1920x1080"
    CHROME_HEADLESS: bool = True
    CHROME_OPTIONS: List[str] = [
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1920x1080",
        "--disable-extensions",
        "--disable-notifications"
    ]
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36"

    # Supabase settings
    SUPABASE_URL: str = os.getenv('SUPABASE_URL', '')
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

    def model_post_init(self, *args, **kwargs):
        """Validate required settings after initialization"""
        super().model_post_init(*args, **kwargs)
        if not self.SUPABASE_URL:
            raise ValueError("SUPABASE_URL is required")
        if not self.SUPABASE_SERVICE_ROLE_KEY:
            raise ValueError("SUPABASE_SERVICE_ROLE_KEY is required")

        # Update Chrome options based on headless setting
        if not self.CHROME_HEADLESS:
            self.CHROME_OPTIONS = [opt for opt in self.CHROME_OPTIONS if not opt.startswith("--headless")]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

# Initialize settings
settings = Settings(
    _env_file=Path(__file__).parent.parent.parent / '.env',  # Go up to root directory
)