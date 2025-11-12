[![CI](https://github.com/Shakour-Data/39-logging-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/39-logging-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/39-logging-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/39-logging-service/actions/workflows/cd.yml)

# 39-logging-service

Centralized log aggregation

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8141 --reload
```

## Port
- **Service Port:** 8141

## Database
- **Type:** ElasticSearch

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8141/docs
- Redoc: http://localhost:8141/redoc

