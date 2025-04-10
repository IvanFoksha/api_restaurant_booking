from typing import Generator

from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)


def get_session() -> Generator[Session, None, None]:
    """
    Get database session.
    
    Yields:
        Session: Database session
    """
    with Session(engine) as session:
        yield session 