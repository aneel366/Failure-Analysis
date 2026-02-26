# Failure Analysis: FastAPI + React + Docker

## What is included
- FastAPI backend with:
  - station risk scoring
  - cluster detection
  - 3-month ARIMA forecast endpoint
  - lightning risk model endpoint
- React dashboard wireframe with 5 requested panels
- Dockerfiles + docker-compose for local deployment

## Run with Docker
```bash
docker compose up --build
```

Services:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Postgres: `localhost:5432`

## Key API routes
- `GET /failures/station-risk`
- `GET /failures/clusters`
- `GET /failures/forecast?steps=3`
- `GET /failures/lightning-risk-model`
