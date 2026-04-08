from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class HealthCheck(Base):
    """SQLAlchemy ORM model for the health_logs table."""

    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(50))
    status_code = Column(Integer)
    latency_ms = Column(Float)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
