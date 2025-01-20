from pydantic_settings import BaseSettings
from typing import Optional, List
import socket
import os
from pathlib import Path

class Settings(BaseSettings):
    # Router settings
    ROUTER_URL: str = "http://192.168.100.1/html/bbsp/pcp/pcp.asp"
    ROUTER_USERNAME: str = "Digicel"
    ROUTER_PASSWORD: str = "Digicel"

    # Application settings
    DUMP_PATH: str = "./data"
    LOG_LEVEL: str = "INFO"
    REFRESH_INTERVAL: int = 300
    CHROME_WINDOW_SIZE: str = "1920x1080"

    # Chrome settings - these won't come from env vars
    CHROME_OPTIONS: List[str] = [
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-notifications"
    ]
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36"

    @property
    def HOSTNAME(self) -> str:
        return socket.gethostname()

    @property
    def OUTPUT_DIR(self) -> Path:
        return Path(self.DUMP_PATH) / f"{self.HOSTNAME}-ports"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from env file

settings = Settings()