from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes.health import router as health_router

app = FastAPI(
    title="Pulse-Check API",
    description="A lightweight DevOps health monitoring service",
    version="1.0.0",
)

# CORS — allow all origins for now; tighten in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the table exists before serving requests.
Base.metadata.create_all(bind=engine)

# Register route handlers.
app.include_router(health_router)
