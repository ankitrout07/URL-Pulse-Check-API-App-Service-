# 🩺 Pulse-Check API

A lightweight DevOps-centric health monitoring service built with **FastAPI** and **PostgreSQL**. This application tracks service uptime and latency, storing results in an Azure Database for PostgreSQL Flexible Server and deployed on **Azure App Service**.

---

## 🚀 Features

- **Real-time Logging** — Capture status codes and latency (ms) for external services via a REST endpoint.
- **History Tracking** — Query the last 10 health checks with timestamps.
- **Cloud Ready** — Optimized for deployment on Azure App Service with environment-based configuration.
- **CI/CD Pipeline** — Automated build and deploy via GitHub Actions.
- **Infrastructure as Code** — Full Azure infrastructure provisioned with Terraform.

---

## 🛠️ Tech Stack

| Layer            | Technology                         |
| ---------------- | ---------------------------------- |
| **Framework**    | FastAPI (Python 3.11+)             |
| **Database**     | PostgreSQL (Azure Flexible Server) |
| **ORM**          | SQLAlchemy 2.0                     |
| **Validation**   | Pydantic v2                        |
| **Infrastructure** | Terraform (AzureRM ~> 3.0)       |
| **CI/CD**        | GitHub Actions                     |
| **Container**    | Docker (Python 3.11-slim)          |

---

## 📂 Project Structure

```text
pulse-check/
├── app/
│   ├── __init__.py            # Package marker
│   ├── main.py                # FastAPI app instance, CORS, startup
│   ├── database.py            # SQLAlchemy engine & session config
│   ├── models.py              # ORM models (health_logs table)
│   ├── schemas.py             # Pydantic request/response schemas
│   └── routes/
│       ├── __init__.py
│       └── health.py          # API route handlers
├── tests/
│   ├── __init__.py
│   └── test_api.py            # Endpoint tests (pytest + SQLite)
├── infra/
│   ├── main.tf                # Azure resources (RG, App Service, PostgreSQL)
│   ├── variables.tf           # Input variables
│   ├── outputs.tf             # Output values (webapp URL, DB FQDN)
│   └── terraform.tfvars       # Non-sensitive variable values
├── .github/
│   └── workflows/
│       └── deploy.yml         # Build & deploy pipeline
├── Dockerfile                 # Container image definition
├── requirements.txt           # Pinned Python dependencies
├── .env.example               # Environment variable template
├── .gitignore
├── .dockerignore
└── README.md
```

---

## 📡 API Endpoints

| Method | Path           | Description                          |
| ------ | -------------- | ------------------------------------ |
| `GET`  | `/`            | Health status of the API itself      |
| `POST` | `/log-health`  | Log a service health check result    |
| `GET`  | `/history`     | Retrieve the 10 most recent logs     |

### `POST /log-health` — Request Body

```json
{
  "service": "my-service",
  "code": 200,
  "latency": 42.5
}
```

### `GET /history` — Response Example

```json
[
  {
    "id": 1,
    "service_name": "my-service",
    "status_code": 200,
    "latency_ms": 42.5,
    "timestamp": "2026-04-08T12:00:00Z"
  }
]
```

---

## ⚡ Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- PostgreSQL (or use the Docker setup)

### 1. Clone & Set Up

```bash
git clone https://github.com/ankitrout07/URL-Pulse-Check-API-App-Service-.git
cd URL-Pulse-Check-API-App-Service-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and set your DATABASE_URL
```

### 3. Run the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

---

## 🐳 Docker

```bash
docker build -t pulse-check-api .
docker run -p 8000:8000 -e DATABASE_URL="postgresql://user:pass@host:5432/dbname" pulse-check-api
```

---

## 🧪 Running Tests

Tests use an in-memory SQLite database — no external database required.

```bash
source venv/bin/activate
pytest tests/ -v
```

---

## 🏗️ Infrastructure (Terraform)

The `infra/` directory provisions the following Azure resources:

| Resource                          | SKU / Tier        |
| --------------------------------- | ----------------- |
| Resource Group                    | —                 |
| App Service Plan                  | B1 (Linux)        |
| Linux Web App                     | Python 3.11       |
| PostgreSQL Flexible Server        | B_Standard_B1ms   |
| PostgreSQL Firewall Rule          | Allow Azure Services |

### Deploy Infrastructure

```bash
cd infra

# Set the database password securely
export TF_VAR_db_password="YourSecurePasswordHere"

terraform init
terraform plan
terraform apply
```

> ⚠️ **Never commit secrets to `terraform.tfvars`.** Use `TF_VAR_` environment variables or a secrets manager.

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`) runs on every push to `main`:

1. **Build** — Checks out code, installs Python 3.11, installs dependencies, zips the artifact.
2. **Deploy** — Downloads the artifact and deploys to Azure App Service using a publish profile.

### Required Secrets

| Secret                            | Description                              |
| --------------------------------- | ---------------------------------------- |
| `AZURE_WEBAPP_PUBLISH_PROFILE`    | Azure App Service publish profile XML    |

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).