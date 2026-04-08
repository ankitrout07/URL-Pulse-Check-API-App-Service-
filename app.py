from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import Session

from database import Base, engine, get_db

app = FastAPI()

# Ensure the table exists before serving requests.
Base.metadata.create_all(bind=engine)

class HealthCheckCreate(BaseModel):
    service: str = Field(..., max_length=50)
    code: int
    latency: float

class HealthCheckRead(BaseModel):
    id: int
    service_name: str
    status_code: int
    latency_ms: float
    timestamp: datetime

    class Config:
        orm_mode = True

class HealthCheck(Base):
    __tablename__ = "health_logs"
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(50))
    status_code = Column(Integer)
    latency_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

@app.get("/", response_model=dict)
def read_root():
    return {"status": "Pulse-Check API is running"}

@app.post("/log-health", response_model=dict)
def log_health(payload: HealthCheckCreate, db: Session = Depends(get_db)):
    new_log = HealthCheck(
        service_name=payload.service,
        status_code=payload.code,
        latency_ms=payload.latency,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"message": "Log saved successfully", "id": new_log.id}

@app.get("/history", response_model=List[HealthCheckRead])
def get_history(db: Session = Depends(get_db)):
    return db.query(HealthCheck).order_by(HealthCheck.timestamp.desc()).limit(10).all()