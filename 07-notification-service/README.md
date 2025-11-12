# Notification Service

Notification Service for the Gravity MicroServices Platform.

[![CI/CD](https://github.com/Shakour-Data/notification-service/actions/workflows/ci.yml/badge.svg)](https://github.com/Shakour-Data/notification-service/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 📋 Overview

This microservice is part of the Gravity MicroServices Platform, a comprehensive collection of independent, reusable microservices designed for enterprise applications.

**Key Features:**
- Multi-channel notifications (Email
- SMS
- Push)
- notification templates
- delivery tracking
- notification preferences

## 🎯 Service Independence

This service follows the **5 Golden Principles** of microservices:
- ✅ **One Repository = One Service** - Independent Git repository
- ✅ **One Service = One Database** - Dedicated PostgreSQL database
- ✅ **Communication via API Only** - REST API communication
- ✅ **Infrastructure as Code** - Complete Docker setup
- ✅ **Independent Deployment** - Can be deployed standalone

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Poetry (for dependency management)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Shakour-Data/notification-service.git
cd notification-service
```

2. **Install dependencies:**
```bash
poetry install
```

3. **Create environment file:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start the service:**
```bash
poetry run python -m app.main
```

The service will be available at http://localhost:8007

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start service with all dependencies
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

### Using Docker Only

```bash
# Build image
docker build -t  .

# Run container
docker run -d \\
  --name notification-service \\
  -p 8007:8007 \\
  --env-file .env \\
  
```

## ⚙️ Configuration

### Environment Variables

Create a .env file based on .env.example:

```bash
# Service Configuration
SERVICE_NAME=notification-service
SERVICE_PORT=8007
ENVIRONMENT=development

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/notification_service_db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# API Configuration
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
```

### Database Setup

The service uses PostgreSQL with automatic migrations:

```bash
# Run migrations
poetry run alembic upgrade head

# Create new migration
poetry run alembic revision --autogenerate -m "Description"
```

## 📚 API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8007/docs
- **ReDoc**: http://localhost:8007/redoc
- **OpenAPI JSON**: http://localhost:8007/openapi.json

### Main Endpoints

```
GET    /health              - Health check endpoint
GET    /api/v1/...          - Service-specific endpoints
POST   /api/v1/...          - Create operations
PUT    /api/v1/...          - Update operations
DELETE /api/v1/...          - Delete operations
```

## 🧪 Testing

### Run All Tests

```bash
poetry run pytest tests/ -v
```

### Run with Coverage

```bash
poetry run pytest tests/ -v --cov=app --cov-report=html
```

### Run Specific Test Files

```bash
poetry run pytest tests/test_main.py -v
```

### Test Coverage Requirements

- Minimum coverage: **95%**
- All tests must pass before deployment
- Integration tests included

## 🔧 Development

### Project Structure

```
notification-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── api/
│   │   └── v1/              # API endpoints
│   ├── core/
│   │   ├── database.py      # Database connection
│   │   ├── redis_client.py  # Redis client
│   │   └── security.py      # Security utilities
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
├── tests/
│   ├── conftest.py          # Test fixtures
│   └── test_*.py            # Test files
├── alembic/                 # Database migrations
├── docker-compose.yml       # Local infrastructure
├── Dockerfile               # Container image
├── pyproject.toml           # Dependencies
└── README.md                # This file
```

### Code Quality Standards

```bash
# Format code
poetry run black app/ tests/
poetry run isort app/ tests/

# Type checking
poetry run mypy app/

# Linting
poetry run ruff check app/ tests/

# Security scanning
poetry run bandit -r app/
poetry run safety check
```

## 🔐 Security

- **Authentication**: OAuth2 with JWT tokens
- **Authorization**: Role-Based Access Control (RBAC)
- **Data Encryption**: TLS 1.3 for transport
- **Secret Management**: Environment variables (never hardcoded)
- **Input Validation**: Pydantic models
- **SQL Injection Prevention**: Parametrized queries
- **Rate Limiting**: Built-in rate limiting support

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:8007/health
```

Response:
```json
{
  "status": "healthy",
  "service": "notification-service",
  "version": "1.0.0",
  "timestamp": "2025-11-12T10:00:00Z"
}
```

### Metrics

Prometheus metrics available at:
```
GET /metrics
```

## 🚀 Deployment

### Production Deployment

1. **Set environment variables:**
```bash
export ENVIRONMENT=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=your-production-database-url
```

2. **Run migrations:**
```bash
poetry run alembic upgrade head
```

3. **Start with production settings:**
```bash
poetry run gunicorn app.main:app \\
  --workers 4 \\
  --worker-class uvicorn.workers.UvicornWorker \\
  --bind 0.0.0.0:8007
```

### Kubernetes Deployment

Kubernetes manifests are available in the k8s/ directory:

```bash
kubectl apply -f k8s/
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'feat: add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: resolve bug
refactor: restructure code
docs: update documentation
test: add tests
chore: update dependencies
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Services

Part of the Gravity MicroServices Platform:
- [API Gateway](https://github.com/Shakour-Data/api-gateway)
- [Service Discovery](https://github.com/Shakour-Data/service-discovery)
- [Common Library](https://github.com/Shakour-Data/common-library)

## 📧 Support

For support, please open an issue on GitHub or contact the development team.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Poetry](https://python-poetry.org/) - Dependency management
- [Docker](https://www.docker.com/) - Containerization

---

**Made with ❤️ by the Gravity MicroServices Team**
