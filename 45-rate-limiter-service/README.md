[![CI](https://github.com/Shakour-Data/45-rate-limiter-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/45-rate-limiter-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/45-rate-limiter-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/45-rate-limiter-service/actions/workflows/cd.yml)

# 45-rate-limiter-service

Distributed rate limiting

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8147 --reload
```

## Port
- **Service Port:** 8147

## Database
- **Type:** Redis

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8147/docs
- Redoc: http://localhost:8147/redoc

