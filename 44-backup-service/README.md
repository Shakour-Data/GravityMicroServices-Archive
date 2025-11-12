[![CI](https://github.com/Shakour-Data/44-backup-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/44-backup-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/44-backup-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/44-backup-service/actions/workflows/cd.yml)

# 44-backup-service

Automated backup and restore

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8146 --reload
```

## Port
- **Service Port:** 8146

## Database
- **Type:** PostgreSQL+S3

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8146/docs
- Redoc: http://localhost:8146/redoc

