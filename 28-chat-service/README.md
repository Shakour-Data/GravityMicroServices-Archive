[![CI](https://github.com/Shakour-Data/28-chat-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/28-chat-service/actions/workflows/ci.yml)
[![CD](https://github.com/Shakour-Data/28-chat-service/actions/workflows/cd.yml/badge.svg)](https://github.com/Shakour-Data/28-chat-service/actions/workflows/cd.yml)

# 28-chat-service

Real-time messaging with WebSocket

## Quick Start

```bash
# Install dependencies
poetry install

# Run service
poetry run uvicorn app.main:app --port 8120 --reload
```

## Port
- **Service Port:** 8120

## Database
- **Type:** PostgreSQL+Redis

## Status
⏳ Ready for development

## Documentation
- API Docs: http://localhost:8120/docs
- Redoc: http://localhost:8120/redoc

