from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from datetime import datetime

app = FastAPI()

# Database Connection (Environment variables used for App Service)
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Schema
class HealthCheck(Base):
    __tablename__ = "health_logs"
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(50))
    status_code = Column(Integer)
    latency_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"status": "Pulse-Check API is running"}

@app.post("/log-health")
def log_health(service: str, code: int, latency: float, db: Session = Depends(lambda: SessionLocal())):
    new_log = HealthCheck(service_name=service, status_code=code, latency_ms=latency)
    db.add(new_log)
    db.commit()
    return {"message": "Log saved successfully"}

@app.get("/history")
def get_history(db: Session = Depends(lambda: SessionLocal())):
    return db.query(HealthCheck).order_by(HealthCheck.timestamp.desc()).limit(10).all()