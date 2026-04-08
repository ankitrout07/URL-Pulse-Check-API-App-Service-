import os

# Set a dummy DATABASE_URL before importing the app so the database module
# doesn't raise during test collection.  SQLite is used for test isolation.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# ---------- Test database setup ----------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ---------- Tests ----------

def test_root():
    """GET / should return a running status message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Pulse-Check API is running"}


def test_log_health():
    """POST /log-health should persist a record and return its id."""
    payload = {"service": "test-svc", "code": 200, "latency": 42.5}
    response = client.post("/log-health", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Log saved successfully"
    assert "id" in data


def test_history():
    """GET /history should return a list of recent health checks."""
    response = client.get("/history")
    assert response.status_code == 200
    records = response.json()
    assert isinstance(records, list)
    assert len(records) >= 1  # at least the one we just created


def test_history_fields():
    """Each history record should contain the expected fields."""
    # Insert a record first
    client.post("/log-health", json={"service": "field-test", "code": 503, "latency": 99.1})
    response = client.get("/history")
    record = response.json()[0]
    assert "id" in record
    assert "service_name" in record
    assert "status_code" in record
    assert "latency_ms" in record
    assert "timestamp" in record
