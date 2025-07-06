from pydantic_settings import BaseSettings
from typing import Optional
import logging

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # Default algorithm for JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Default expiration time for access

    LOG_LEVEL: str = "INFO"  # Default log level

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings() # type: ignore

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[1;36m',     # Bold Cyan
        'INFO': '\033[1;32m',      # Bold Green
        'WARNING': '\033[1;33m',   # Bold Yellow
        'ERROR': '\033[1;31m',     # Bold Red
        'CRITICAL': '\033[1;41m',  # Bold background red
    }
    RESET = '\033[0m'

    def format(self, record):  # type: ignore[override]
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


class CLogger:
    def __init__(self, name: Optional[str] = None):
        match settings.LOG_LEVEL.upper():
            case "DEBUG":
                level = logging.DEBUG
            case "INFO":
                level = logging.INFO
            case "WARNING":
                level = logging.WARNING
            case "ERROR":
                level = logging.ERROR
            case "CRITICAL":
                level = logging.CRITICAL
            case _:
                print(f"Invalid log level: {settings.LOG_LEVEL}. Defaulting to INFO.")
                level = logging.INFO

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid adding multiple handlers if logger already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = ColorFormatter(
                '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
