"""
Database connection — SQLite by default.
To switch to PostgreSQL:
  pip install psycopg2-binary
  DATABASE_URL = "postgresql://user:password@localhost/signapp"
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./signapp.db"    # file created in backend/

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}   # needed for SQLite only
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
