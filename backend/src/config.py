from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    database_url: str = "postgresql://localhost/todo_backend"
    environment: str = "development"
    log_level: str = "info"
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "your-default-secret-key-change-in-production")
    access_token_expire_minutes: int = 43200  # 30 days in minutes (30 * 24 * 60)

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()