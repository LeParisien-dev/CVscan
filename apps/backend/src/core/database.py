import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment: "local" (Mac) or "docker" (inside docker-compose)
ENV = os.getenv("ENV", "local")

DB_USER = os.getenv("DATABASE_USER", "cvscan")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "cvscan_pass")
DB_NAME = os.getenv("DATABASE_NAME", "cvscan_db")
DB_PORT = os.getenv("DATABASE_PORT", "5432")

# Auto-select DB host depending on environment
if ENV == "docker":
    DB_HOST = "postgres"
else:
    DB_HOST = "localhost"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session (for FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
