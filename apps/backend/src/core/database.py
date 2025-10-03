import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Priority: DATABASE_URL if explicitly set (Render/Neon)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    ENV = os.getenv("ENV", "local")
    DB_USER = os.getenv("DATABASE_USER", "cvscan")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "cvscan_pass")
    DB_NAME = os.getenv("DATABASE_NAME", "cvscan_db")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")

    if ENV == "docker":
        DB_HOST = "postgres"
    else:
        DB_HOST = "localhost"

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
