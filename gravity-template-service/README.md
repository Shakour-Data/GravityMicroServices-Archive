# Gravity Template Service

> **Template repository for creating new Gravity microservices**

This is a template repository for the Gravity MicroServices Platform. Use this template to create new microservices with all the standard structure, configurations, and best practices built-in.

## 🚀 Quick Start

### 1. Create New Service from Template

**On GitHub:**
```bash
# Click "Use this template" button on GitHub
# Or use GitHub CLI:
gh repo create GravityMicroServices/gravity-your-service --template GravityMicroServices/gravity-template-service
```

**Locally:**
```bash
# Clone this template
git clone https://github.com/GravityMicroServices/gravity-template-service gravity-your-service
cd gravity-your-service

# Remove template git history
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"
```

### 2. Customize Service

Replace placeholders in the following files:

- `README.md`: Update service name and description
- `pyproject.toml`: Change `name`, `description`, `version`
- `app/config.py`: Update `SERVICE_NAME`
- `.env.example`: Set `SERVICE_NAME` and `PORT`
- `docker-compose.yml`: Update service names and ports

**Quick Replace Script:**
```bash
# Replace SERVICE_NAME placeholder
$serviceName = "your-service"
$port = "8010"

Get-ChildItem -Recurse -File | ForEach-Object {
    (Get-Content $_.FullName) -replace 'SERVICE_NAME', $serviceName -replace 'SERVICE_PORT', $port | Set-Content $_.FullName
}
```

### 3. Install Dependencies

```bash
# Install Poetry (if not installed)
pip install poetry

# Install dependencies
poetry install

# Or with pip
pip install -r requirements.txt
```

### 4. Setup Database

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head
```

### 5. Run Service

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --port 8000

# Or with Poetry
poetry run uvicorn app.main:app --reload --port 8000

# Or with Docker
docker-compose up app
```

### 6. Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

---

## 📁 Project Structure

```
gravity-your-service/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Continuous Integration
│       ├── cd.yml                    # Continuous Deployment
│       └── security.yml              # Security scanning
│
├── app/
│   ├── __init__.py
│   ├── main.py                       # FastAPI application
│   ├── config.py                     # Configuration from env
│   ├── dependencies.py               # FastAPI dependencies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints.py          # API endpoints
│   │       └── router.py             # Router aggregation
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py               # Database connection
│   │   ├── redis_client.py           # Redis connection
│   │   ├── security.py               # Auth helpers
│   │   ├── exceptions.py             # Custom exceptions
│   │   └── logging_config.py         # Structured logging
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── example.py                # SQLAlchemy models
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── example.py                # Pydantic schemas
│   │   └── response.py               # Response schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── example_service.py        # Business logic
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Test fixtures
│   ├── test_main.py                  # Main tests
│   ├── integration/
│   │   └── test_api.py               # Integration tests
│   └── unit/
│       └── test_services.py          # Unit tests
│
├── alembic/
│   ├── versions/                     # Database migrations
│   ├── env.py
│   └── script.py.mako
│
├── k8s/
│   ├── deployment.yaml               # Kubernetes deployment
│   ├── service.yaml                  # Kubernetes service
│   ├── configmap.yaml                # Configuration
│   ├── secrets.yaml.example          # Secrets template
│   ├── ingress.yaml                  # Ingress rules
│   └── hpa.yaml                      # Horizontal Pod Autoscaler
│
├── scripts/
│   ├── __init__.py
│   ├── dev.py                        # Development server
│   └── migrate.py                    # Database migrations
│
├── .env.example                      # Environment template
├── .gitignore
├── alembic.ini                       # Alembic configuration
├── docker-compose.yml                # Local development
├── Dockerfile                        # Container image
├── pyproject.toml                    # Dependencies (Poetry)
├── pytest.ini                        # Pytest configuration
├── README.md                         # This file
├── DEPLOYMENT.md                     # Deployment guide
└── LICENSE                           # MIT License
```

---

## 🛠️ Development

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html

# Specific test file
pytest tests/test_main.py -v

# Watch mode (requires pytest-watch)
ptw -- -v
```

### Code Quality

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
ruff app/ tests/

# Type checking
mypy app/

# All quality checks
black app/ tests/ && isort app/ tests/ && ruff app/ tests/ && mypy app/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Show migration history
alembic history
```

---

## 🐳 Docker

### Build Image

```bash
# Build
docker build -t gravity-your-service:latest .

# Build with specific tag
docker build -t gravity-your-service:1.0.0 .
```

### Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

---

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace gravity

# Apply configurations
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n gravity

# View logs
kubectl logs -f deployment/your-service -n gravity

# Scale deployment
kubectl scale deployment/your-service --replicas=5 -n gravity
```

### Update Deployment

```bash
# Update image
kubectl set image deployment/your-service your-service=gravity-your-service:1.0.1 -n gravity

# Rollback
kubectl rollout undo deployment/your-service -n gravity

# Check rollout status
kubectl rollout status deployment/your-service -n gravity
```

---

## 📊 Monitoring

### Health Check

```bash
# Health endpoint
curl http://localhost:8000/health

# Detailed health check
curl http://localhost:8000/health/detailed
```

### Metrics

```bash
# Prometheus metrics
curl http://localhost:9090/metrics
```

### Logs

```bash
# View logs (Docker)
docker-compose logs -f app

# View logs (Kubernetes)
kubectl logs -f deployment/your-service -n gravity

# Structured logging
# All logs are in JSON format for easy parsing
```

---

## 🔒 Security

### Environment Variables

Never commit `.env` file! Always use `.env.example` as template.

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env
```

### Secrets Management

For production, use:
- **Kubernetes Secrets**: `kubectl create secret`
- **HashiCorp Vault**: Centralized secrets
- **AWS Secrets Manager**: Cloud secrets
- **Azure Key Vault**: Azure secrets

### Security Scanning

```bash
# Scan dependencies
safety check

# Scan code for security issues
bandit -r app/

# Scan Docker image
trivy image gravity-your-service:latest
```

---

## 🤝 Contributing

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run Quality Checks**
   ```bash
   pytest tests/ -v --cov=app
   black app/ tests/
   isort app/ tests/
   mypy app/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature
   # Create PR on GitHub
   ```

---

## 📝 API Documentation

### Swagger UI
- **URL**: http://localhost:8000/docs
- Interactive API documentation
- Try out endpoints directly

### ReDoc
- **URL**: http://localhost:8000/redoc
- Alternative API documentation
- Clean, readable format

### OpenAPI Schema
- **URL**: http://localhost:8000/openapi.json
- Machine-readable API schema
- Import into tools like Postman

---

## 🔗 Integration with Other Services

### Service Discovery

```python
# Register with Consul
await service_registry.register(
    name="your-service",
    port=8000,
    health_check_url="/health"
)

# Discover other services
auth_service_url = await service_registry.get_service_url("auth-service")
```

### Event Publishing

```python
# Publish event
await event_bus.publish("resource.created", {
    "resource_id": resource.id,
    "user_id": user.id,
    "timestamp": datetime.utcnow().isoformat()
})
```

### Event Consuming

```python
# Subscribe to events
@event_bus.subscribe("user.created")
async def handle_user_created(event: dict):
    # Handle event
    pass
```

---

## 🎯 Best Practices

### Code Style
- ✅ Follow PEP 8
- ✅ Use type hints everywhere
- ✅ Write docstrings for all functions
- ✅ Keep functions small and focused
- ✅ Use meaningful variable names

### Testing
- ✅ Minimum 95% code coverage
- ✅ Write tests first (TDD)
- ✅ Test edge cases
- ✅ Mock external dependencies
- ✅ Use fixtures for common setup

### Security
- ✅ Validate all inputs
- ✅ Use parametrized queries
- ✅ Never hardcode secrets
- ✅ Implement rate limiting
- ✅ Use HTTPS in production

### Performance
- ✅ Use async/await for I/O
- ✅ Implement caching
- ✅ Optimize database queries
- ✅ Use connection pooling
- ✅ Monitor performance metrics

---

## 📚 Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

### Gravity Platform
- [Architecture Guide](../docs/COMPLETE_ARCHITECTURE.md)
- [Configuration Guide](../docs/STANDARD_CONFIGURATIONS.md)
- [Development Patterns](../docs/DEVELOPMENT_PATTERNS.md)
- [Team Standards](../docs/TEAM_PROMPT.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/GravityMicroServices/gravity-your-service/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GravityMicroServices/gravity-your-service/discussions)
- **Email**: support@gravitymicroservices.io

---

**Built with ❤️ by the Gravity Elite Engineering Team**
