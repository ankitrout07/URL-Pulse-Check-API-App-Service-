from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HealthCheck
from app.schemas import HealthCheckCreate, HealthCheckRead

router = APIRouter()


@router.get("/", response_model=dict)
def read_root():
    """Root endpoint — returns API status."""
    return {"status": "Pulse-Check API is running"}


@router.post("/log-health", response_model=dict)
def log_health(payload: HealthCheckCreate, db: Session = Depends(get_db)):
    """Log a health check result to the database."""
    new_log = HealthCheck(
        service_name=payload.service,
        status_code=payload.code,
        latency_ms=payload.latency,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"message": "Log saved successfully", "id": new_log.id}


@router.get("/history", response_model=List[HealthCheckRead])
def get_history(db: Session = Depends(get_db)):
    """Return the 10 most recent health check logs."""
    return db.query(HealthCheck).order_by(HealthCheck.timestamp.desc()).limit(10).all()
