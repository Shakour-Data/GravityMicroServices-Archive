[![CI](https://github.com/Shakour-Data/40-scheduler-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/40-scheduler-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/40-scheduler-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/40-scheduler-service/actions/workflows/cd.yml)

# 40-scheduler-service

Job scheduling and background tasks

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8142 --reload
```

## Port
- **Service Port:** 8142

## Database
- **Type:** PostgreSQL+Redis

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8142/docs
- Redoc: http://localhost:8142/redoc

