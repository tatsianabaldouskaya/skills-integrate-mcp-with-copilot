from sqlmodel import SQLModel, create_engine, Session
from typing import Optional
import os

# Use a local SQLite DB file by default. This keeps setup trivial for dev.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./activities.db")

engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
