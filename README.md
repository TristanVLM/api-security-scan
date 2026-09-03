# API Security Scan

> A personal cybersecurity project for building an API vulnerability scanner
> and improving my application security skills.

## About the Project

API Security Scan is a full-stack project in progress. The goal is to build a
platform that can assess REST APIs against the
[OWASP API Security Top 10](https://owasp.org/API-Security/), centralize scan
results, and display them through a React dashboard.

This project is based on the original
[API Security Scanner project by CarterPerez-dev](https://github.com/CarterPerez-dev/Cybersecurity-Projects/tree/main/PROJECTS/intermediate/api-security-scanner).
I am using it as a learning foundation and plan to extend it with additional
features, stronger security controls, improved testing, and a more complete
user experience than the original implementation.

## Project Direction

The purpose of this repository is not only to reproduce the base project, but
to understand its design and progressively improve it. Planned improvements
include:

- a modular scanner architecture with reusable vulnerability checks;
- configurable targets, payloads, headers, authentication, and scan policies;
- more precise detection rules with evidence for every finding;
- scan history, endpoint-level results, severity levels, and exportable reports;
- stronger authentication, authorization, rate limiting, and secret handling;
- automated tests covering both the API and the scanner engine;
- a React dashboard focused on clear, actionable security findings;
- improved Docker-based development and deployment workflows.

## Current Features

- FastAPI application with health endpoints (`/` and `/health`);
- user registration and login (`/auth/register`, `/auth/login`);
- email and password validation with Pydantic;
- JWT access token generation;
- password hashing with bcrypt;
- PostgreSQL persistence through SQLAlchemy;
- Docker Compose development environment with PostgreSQL;
- OpenAPI documentation through `/docs` and `/redoc`.

## Roadmap

- [ ] Add scan targets and scan configuration management;
- [ ] Implement SQL injection, authentication, IDOR, and rate-limit modules;
- [ ] Add configurable payloads and detection rules;
- [ ] Cover the OWASP API Security Top 10 progressively;
- [ ] Store scan history and endpoint-level vulnerability reports;
- [ ] Build the React dashboard;
- [ ] Add automated tests and exportable reports;
- [ ] Add production security hardening and CI checks.

## Architecture

```text
.
├── backend/
│   ├── core/           # Database, security, and FastAPI dependencies
│   ├── models/         # SQLAlchemy models
│   ├── repositories/   # Data access layer
│   ├── routes/         # HTTP endpoints
│   ├── schemas/        # Pydantic validation schemas
│   ├── services/       # Business logic
│   ├── factory.py      # Application creation and configuration
│   ├── main.py         # Uvicorn entry point
│   └── requirements.txt
├── conf/docker/        # Backend Dockerfile
├── dev.compose.yml     # PostgreSQL and backend services
└── .env.example        # Documented environment variables
```

## Technology Stack

| Area | Technologies |
| --- | --- |
| Backend | Python 3.11, FastAPI, Uvicorn |
| Validation | Pydantic, email-validator |
| Database | PostgreSQL 16, SQLAlchemy, psycopg2 |
| Authentication | JWT, bcrypt |
| DevOps | Docker, Docker Compose |
| Planned frontend | React |

## Getting Started with Docker

### Prerequisites

- Docker;
- Docker Compose v2.

### Setup

```bash
git clone <repository-url>
cd api-security-scan
cp .env.example .env
```

Replace `SECRET_KEY` in `.env` with a long, randomly generated value before
using the project outside local development.

### Start the services

```bash
docker compose -f dev.compose.yml up --build
```

The API is available at http://localhost:8000.

```bash
curl http://localhost:8000/health
```

Stop the services:

```bash
docker compose -f dev.compose.yml down
```

Remove the local PostgreSQL data as well:

```bash
docker compose -f dev.compose.yml down -v
```

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
cd backend
uvicorn main:app --reload
```

Local development requires a `.env` file containing at least `DATABASE_URL`
and `SECRET_KEY`. When the backend connects to PostgreSQL through Docker
Compose, the database host is the service name `db`.

## API Usage

Interactive documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Register a user:

```bash
curl -X POST http://localhost:8000/auth/register \
	-H "Content-Type: application/json" \
	-d '{"email":"analyst@example.com","password":"SecurePass1"}'
```

Log in:

```bash
curl -X POST http://localhost:8000/auth/login \
	-H "Content-Type: application/json" \
	-d '{"email":"analyst@example.com","password":"SecurePass1"}'
```

## Learning and Responsible Use

This project is developed for learning and portfolio purposes. Security tests
must only be performed against APIs that you own or for which you have explicit
authorization.
