"""Database engine and session configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.settings import DATABASE_URL_SYNC, LOG_LEVEL

# Create engine with sync driver (psycopg2)
engine = create_engine(
    DATABASE_URL_SYNC,
    echo=LOG_LEVEL == "DEBUG",
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()


def init_db():
    """Initialize database - create all tables."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
