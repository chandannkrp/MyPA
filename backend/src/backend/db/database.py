from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings
from backend.core.logging import logger

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)

logger.info("Database engine created successfully.")

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass