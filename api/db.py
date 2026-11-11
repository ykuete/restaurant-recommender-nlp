"""Feedback storage: a single table behind DATABASE_URL.

SQLite file locally (sqlite:///feedback.db). In production use a hosted
Postgres such as Neon, because container disks are not persistent:
DATABASE_URL=postgresql://user:password@host/dbname
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    insert,
)
from sqlalchemy.engine import Engine

metadata = MetaData()

feedback_table = Table(
    "feedback",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("business_id", String(64), nullable=False),
    Column("query", Text, nullable=False),
    Column("helpful", Boolean, nullable=False),
)


def normalize_url(url: str) -> str:
    """Hosted Postgres URLs start with postgres:// or postgresql://; use psycopg 3."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix) :]
    return url


def connect(url: str) -> Engine:
    engine = create_engine(normalize_url(url), pool_pre_ping=True)
    metadata.create_all(engine)
    return engine


def save_feedback(engine: Engine, business_id: str, query: str, helpful: bool) -> None:
    with engine.begin() as conn:
        conn.execute(
            insert(feedback_table).values(
                created_at=datetime.now(UTC),
                business_id=business_id,
                query=query,
                helpful=helpful,
            )
        )
