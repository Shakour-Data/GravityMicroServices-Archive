[![CI](https://github.com/Shakour-Data/47-feature-flag-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/47-feature-flag-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/47-feature-flag-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/47-feature-flag-service/actions/workflows/cd.yml)

# 47-feature-flag-service

Feature toggles and gradual rollout

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8149 --reload
```

## Port
- **Service Port:** 8149

## Database
- **Type:** PostgreSQL+Redis

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8149/docs
- Redoc: http://localhost:8149/redoc

