[![CI](https://github.com/Shakour-Data/30-geolocation-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/30-geolocation-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/30-geolocation-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/30-geolocation-service/actions/workflows/cd.yml)

# 30-geolocation-service

Location tracking and geofencing

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8122 --reload
```

## Port
- **Service Port:** 8122

## Database
- **Type:** PostgreSQL+PostGIS

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8122/docs
- Redoc: http://localhost:8122/redoc

