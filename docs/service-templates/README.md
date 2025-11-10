# 📚 Service Documentation Templates

These templates are used to generate consistent documentation for all Gravity microservices.

## Variables to Replace

- `{{SERVICE_NAME}}` - Service name (e.g., "Auth Service", "API Gateway")
- `{{SERVICE_ID}}` - Service ID (e.g., "auth-service", "api-gateway")
- `{{SERVICE_PORT}}` - Default port (e.g., "8081", "8000")
- `{{SERVICE_DESCRIPTION}}` - Brief description
- `{{DATABASE_NAME}}` - Database name (e.g., "auth_db", "gateway_db")
- `{{MAIN_AUTHOR}}` - Primary author name
- `{{CREATED_DATE}}` - Creation date (YYYY-MM-DD)

## Usage

Use the PowerShell script to generate documentation:

```powershell
.\scripts\generate-service-docs.ps1 -ServiceId "api-gateway" -ServiceName "API Gateway" -Port 8000
```

## Templates

- `API.md.template` - Complete API documentation
- `ARCHITECTURE.md.template` - System architecture
- `DEPLOYMENT.md.template` - Deployment guide
- `TESTING.md.template` - Testing guide
- `README.md.template` - Service README
- `CHANGELOG.md.template` - Version history
