from typing import Optional, Any, Generator
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
import secrets
from functools import lru_cache
from sqlmodel import Session, create_engine


class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Restaurant Booking API"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Database settings
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "restaurant_booking"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(
        cls, v: Optional[str], info: Any
    ) -> Optional[PostgresDsn]:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"/{info.data.get('POSTGRES_DB') or ''}",
        )

    def get_session(self) -> Generator[Session, None, None]:
        engine = create_engine(str(self.SQLALCHEMY_DATABASE_URI))
        with Session(engine) as session:
            yield session

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
