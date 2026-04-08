from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HealthCheckCreate(BaseModel):
    """Request schema for logging a health check."""

    service: str = Field(..., max_length=50)
    code: int
    latency: float


class HealthCheckRead(BaseModel):
    """Response schema for reading a health check record."""

    id: int
    service_name: str
    status_code: int
    latency_ms: float
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
