from pydantic_settings import BaseSettings
from typing import Optional
import socket
import os
from pathlib import Path

class Settings(BaseSettings):
    # Router settings
    ROUTER_URL: str = "http://192.168.100.1/html/bbsp/pcp/pcp.asp"
    ROUTER_USERNAME: str = "Digicel"
    ROUTER_PASSWORD: str = "Digicel"

    # Chrome settings
    CHROME_OPTIONS: list = [
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1920x1080",
        "--disable-extensions",
        "--disable-notifications"
    ]
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36"

    # Output settings
    HOSTNAME: str = socket.gethostname()
    BASE_PATH: Path = Path(os.getenv('DUMP_PATH', '/app/data'))
    OUTPUT_DIR: Path = BASE_PATH / f"{HOSTNAME}-ports"

    # Application settings
    REFRESH_INTERVAL: int = 300  # 5 minutes in seconds
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()