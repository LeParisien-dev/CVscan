from sqlalchemy import Column, String, Text
from src.core.database import Base
import uuid

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True
    )
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
