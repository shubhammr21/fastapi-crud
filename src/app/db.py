import os

from databases import Database
from sqlalchemy import create_engine, MetaData
import sqlalchemy as sa

DATABASE_URL = os.environ.get("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

notes = sa.Table(
    "notes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(255), nullable=False),
    sa.Column("content", sa.Text, nullable=False),
    sa.Column("created_at", sa.DateTime, default=sa.func.now(), nullable=False),
)

database = Database(DATABASE_URL)
