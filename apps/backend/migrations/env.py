from __future__ import with_statement
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# --- PATH SETUP ---
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

# --- Import Base metadata ---
from src.core.database import Base

# --- Alembic Config ---
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# --- Helper to build DB URL ---
def get_url():
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    # fallback if DATABASE_URL missing
    ENV = os.getenv("ENV", "local")
    DB_USER = os.getenv("DATABASE_USER", "cvscan")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "cvscan_pass")
    DB_NAME = os.getenv("DATABASE_NAME", "cvscan_db")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    DB_HOST = "postgres" if ENV == "docker" else "localhost"
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Migration logic ---
def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
