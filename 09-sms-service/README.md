[![CI](https://github.com/Shakour-Data/09-sms-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/09-sms-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/09-sms-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/09-sms-service/actions/workflows/cd.yml)

# 09-sms-service

SMS delivery via Twilio/AWS SNS

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8087 --reload
```

## Port
- **Service Port:** 8087

## Database
- **Type:** PostgreSQL

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8087/docs
- Redoc: http://localhost:8087/redoc

