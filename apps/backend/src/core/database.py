import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

# --- Database URL logic ---
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    ENV = os.getenv("ENV", "local")
    DB_USER = os.getenv("DATABASE_USER", "cvscan")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "cvscan_pass")
    DB_NAME = os.getenv("DATABASE_NAME", "cvscan_db")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    DB_HOST = "postgres" if ENV == "docker" else "localhost"
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- SQLAlchemy setup ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Dependency for FastAPI ---
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
