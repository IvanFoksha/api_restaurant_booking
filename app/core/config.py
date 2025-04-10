from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
import secrets
from functools import lru_cache


class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Restaurant Booking API"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "restaurant_booking"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Optional[PostgresDsn]:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Notification settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    This function is used as a dependency in FastAPI endpoints.
    """
    return Settings()


settings = get_settings()
