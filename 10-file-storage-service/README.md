[![CI](https://github.com/Shakour-Data/10-file-storage-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/10-file-storage-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/10-file-storage-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/10-file-storage-service/actions/workflows/cd.yml)

# 10-file-storage-service

File upload with CDN integration

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8088 --reload
```

## Port
- **Service Port:** 8088

## Database
- **Type:** PostgreSQL+S3

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8088/docs
- Redoc: http://localhost:8088/redoc

