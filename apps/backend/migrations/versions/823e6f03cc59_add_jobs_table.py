"""add jobs table

Revision ID: 823e6f03cc59
Revises: 
Create Date: 2025-10-03 22:42:46.571770
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '823e6f03cc59'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Create jobs table"""
    op.create_table(
        "jobs",
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("job_id")
    )
    op.create_index("ix_jobs_job_id", "jobs", ["job_id"], unique=True)

def downgrade() -> None:
    """Drop jobs table"""
    op.drop_index("ix_jobs_job_id", table_name="jobs")
    op.drop_table("jobs")
