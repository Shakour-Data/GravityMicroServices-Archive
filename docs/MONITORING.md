# ================================================================================
# Gravity MicroServices Platform - Monitoring Guide
# ================================================================================
# Author: Lars Björkman (DevOps Lead), Takeshi Yamamoto (Performance Engineer)
# Created: 2025-11-07
# Cost: $150 (1 hour)
# ================================================================================

# Monitoring & Observability Stack

Complete monitoring solution for Gravity MicroServices Platform using Prometheus, Grafana, and OpenTelemetry.

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Services   │────▶│  Prometheus  │────▶│   Grafana   │
│  (Metrics)  │     │  (Storage)   │     │  (Dashboards)│
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Alertmanager │
                    │  (Alerts)    │
                    └──────────────┘
```

## 📊 Components

### Prometheus (Metrics Collection)
- **Purpose**: Time-series database for metrics
- **Port**: 9090
- **Configuration**: `config/prometheus.yml`
- **Alert Rules**: `config/prometheus/alerts.yml`
- **Scrape Interval**: 15 seconds
- **Retention**: 15 days

### Grafana (Visualization)
- **Purpose**: Metrics visualization and dashboards
- **Port**: 3000
- **Dashboards**: `config/grafana/dashboards/`
- **Default Credentials**: admin/admin (change on first login)

### Alertmanager (Alerting)
- **Purpose**: Alert routing and notification
- **Port**: 9093
- **Routes**: Slack, Email, PagerDuty

## 📈 Dashboards

### Platform Overview Dashboard
**File**: `config/grafana/dashboards/platform-overview.json`

**Panels**:
1. **HTTP Request Rate** - Requests per second across all services
2. **Response Time (p95)** - 95th percentile latency with thresholds
3. **Error Rate** - Percentage of 5xx errors
4. **Service Health** - UP/DOWN status for each service
5. **Memory Usage** - Memory consumption per service
6. **CPU Usage** - CPU utilization percentage

**Auto-refresh**: 10 seconds  
**Time Range**: Last 1 hour

### Import Dashboard
```bash
# Via Grafana UI
1. Navigate to Dashboards → Import
2. Upload platform-overview.json
3. Select Prometheus datasource
4. Click Import
```

## 🚨 Alert Rules

### Service Health Alerts

#### ServiceDown (Critical)
- **Condition**: Service unavailable for 1 minute
- **Severity**: Critical
- **Team**: Platform

#### HighErrorRate (Warning)
- **Condition**: Error rate > 5% for 5 minutes
- **Severity**: Warning
- **Team**: Platform

#### CriticalErrorRate (Critical)
- **Condition**: Error rate > 10% for 2 minutes
- **Severity**: Critical
- **Team**: Platform

### Performance Alerts

#### HighResponseTime (Warning)
- **Condition**: p95 latency > 200ms for 5 minutes
- **Severity**: Warning
- **Team**: Platform

#### CriticalResponseTime (Critical)
- **Condition**: p95 latency > 500ms for 2 minutes
- **Severity**: Critical
- **Team**: Platform

### Resource Alerts

#### HighMemoryUsage (Warning)
- **Condition**: Memory > 1GB for 5 minutes
- **Severity**: Warning
- **Team**: Platform

#### HighCPUUsage (Warning)
- **Condition**: CPU > 80% for 5 minutes
- **Severity**: Warning
- **Team**: Platform

### Security Alerts

#### SuspiciousAuthenticationActivity (Critical)
- **Condition**: >100 failed logins/second
- **Severity**: Critical
- **Team**: Security

## 📊 Custom Metrics

### Auth Service Metrics

#### Authentication
- `auth_login_attempts_total{status}` - Login attempts (success/failure)
- `auth_login_failures_total{reason}` - Login failures by reason
- `auth_tokens_generated_total{token_type}` - Tokens generated
- `auth_token_validations_total{status}` - Token validations

#### User Management
- `user_registrations_total{status}` - User registrations
- `active_users` - Current active users
- `user_operations_total{operation}` - User CRUD operations

#### Database & Redis
- `db_query_duration_seconds` - Database query latency
- `db_pool_connections_active` - Active DB connections
- `redis_operations_total{operation}` - Redis operations
- `redis_memory_used_bytes` - Redis memory usage

### API Gateway Metrics

#### Routing
- `gateway_routed_requests_total{service,method,status}` - Routed requests
- `gateway_routing_errors_total{service,error_type}` - Routing errors
- `gateway_service_latency_seconds{service,endpoint}` - Service latency

#### Rate Limiting
- `rate_limit_hits_total{client_id,endpoint}` - Rate limit hits
- `rate_limit_blocks_total{client_id,endpoint}` - Rate limit blocks
- `rate_limit_current_usage{client_id,endpoint}` - Current usage

#### Circuit Breaker
- `circuit_breaker_state{service}` - Circuit state (0=closed, 1=open)
- `circuit_breaker_trips_total{service}` - Circuit breaker trips
- `circuit_breaker_failures_total{service}` - Tracked failures

#### Service Registry
- `registered_services` - Number of registered services
- `service_health_status{service}` - Service health (1=healthy, 0=unhealthy)
- `service_discovery_requests_total{service,result}` - Discovery requests

## 🚀 Quick Start

### 1. Start Monitoring Stack
```bash
# Start Prometheus, Grafana, Alertmanager
docker-compose up -d prometheus grafana alertmanager

# Verify services
curl http://localhost:9090/-/healthy  # Prometheus
curl http://localhost:3000/api/health  # Grafana
curl http://localhost:9093/-/healthy  # Alertmanager
```

### 2. Configure Datasource
```bash
# Login to Grafana
http://localhost:3000
Username: admin
Password: admin

# Add Prometheus datasource
1. Configuration → Data Sources → Add data source
2. Select "Prometheus"
3. URL: http://prometheus:9090
4. Click "Save & Test"
```

### 3. Import Dashboards
```bash
# Import platform overview dashboard
1. Dashboards → Import
2. Upload: config/grafana/dashboards/platform-overview.json
3. Select Prometheus datasource
4. Click Import
```

### 4. Verify Metrics
```bash
# Check metrics endpoints
curl http://localhost:8081/metrics  # Auth Service
curl http://localhost:8080/metrics  # API Gateway

# Query Prometheus
http://localhost:9090/graph
Query: rate(http_requests_total[5m])
```

## 📝 Adding Custom Metrics

### In Python Services

```python
from app.core.metrics import (
    auth_login_attempts_total,
    track_login_attempt,
    increment_user_registration
)

# Using counters
auth_login_attempts_total.labels(status='success').inc()

# Using decorators
@track_login_attempt
async def login(username: str, password: str):
    # Login logic
    pass

# Using helper functions
increment_user_registration(success=True)
```

### Define New Metric

```python
from prometheus_client import Counter, Histogram, Gauge

# Counter (always increases)
my_counter = Counter(
    'my_metric_total',
    'Description of metric',
    ['label1', 'label2']
)

# Gauge (can go up/down)
my_gauge = Gauge(
    'my_current_value',
    'Current value of something'
)

# Histogram (distribution)
my_histogram = Histogram(
    'my_duration_seconds',
    'Duration in seconds',
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0]
)
```

## 🔍 Query Examples

### Request Rate
```promql
rate(http_requests_total[5m])
```

### Error Rate
```promql
rate(http_requests_total{status_code=~"5.."}[5m]) 
/ 
rate(http_requests_total[5m]) * 100
```

### P95 Latency
```promql
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[5m])
) * 1000
```

### Service Health
```promql
up{job=~"auth-service|api-gateway"}
```

### Memory Usage
```promql
process_resident_memory_bytes{job="auth-service"} / 1024 / 1024 / 1024
```

### Top Endpoints by Latency
```promql
topk(10, 
  histogram_quantile(0.95, 
    rate(http_request_duration_seconds_bucket[5m])
  )
) by (endpoint)
```

## 🔔 Alert Configuration

### Alertmanager Config
```yaml
global:
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

route:
  group_by: ['alertname', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'slack'
  
  routes:
  - match:
      severity: critical
    receiver: 'pagerduty'

receivers:
- name: 'slack'
  slack_configs:
  - channel: '#alerts'
    title: '{{ .GroupLabels.alertname }}'
    text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

- name: 'pagerduty'
  pagerduty_configs:
  - service_key: 'YOUR_PAGERDUTY_KEY'
```

## 📊 SLA Monitoring

### Availability Target: 99.9%
```promql
# Monthly uptime percentage
avg_over_time(up{job="auth-service"}[30d]) * 100
```

### Latency Target: p95 < 200ms
```promql
# P95 latency for last 30 days
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[30d])
) * 1000 < 200
```

### Error Rate Target: < 0.1%
```promql
# Error rate for last 30 days
(
  rate(http_requests_total{status_code=~"5.."}[30d])
  /
  rate(http_requests_total[30d])
) * 100 < 0.1
```

## 🔧 Troubleshooting

### Metrics Not Appearing
```bash
# Check Prometheus targets
http://localhost:9090/targets

# Check service metrics endpoint
curl http://localhost:8081/metrics

# Check Prometheus logs
docker logs gravity-prometheus

# Verify scrape config
cat config/prometheus.yml
```

### High Cardinality Issues
```bash
# Check cardinality of metrics
curl http://localhost:9090/api/v1/status/tsdb

# Limit label values
# Bad: user_id as label (millions of users)
# Good: user_tier as label (free, pro, enterprise)
```

### Dashboard Not Loading
```bash
# Check Grafana logs
docker logs gravity-grafana

# Verify datasource connection
Grafana UI → Configuration → Data Sources → Test

# Re-import dashboard
Delete existing → Import new JSON
```

## 📈 Performance Tuning

### Prometheus Optimization
```yaml
# prometheus.yml
global:
  scrape_interval: 15s  # Increase for less precision, lower load
  evaluation_interval: 15s
  
  # External labels for federation
  external_labels:
    cluster: 'production'
    region: 'us-east-1'
```

### Retention Policy
```bash
# Set retention to 30 days
docker run -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus \
  --storage.tsdb.retention.time=30d \
  --storage.tsdb.retention.size=50GB
```

## 📚 Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Alerting Best Practices](https://prometheus.io/docs/practices/alerting/)

## 🎯 Next Steps

1. **OpenTelemetry Integration** - Distributed tracing
2. **Log Aggregation** - ELK/Loki integration
3. **Custom Dashboards** - Service-specific dashboards
4. **SLO Tracking** - Service Level Objectives monitoring
5. **Anomaly Detection** - ML-based anomaly detection

## 👥 Team

- **Lars Björkman** - DevOps Lead - Infrastructure setup
- **Takeshi Yamamoto** - Performance Engineer - Metrics design

## 💰 Cost

- Development: 5 hours × $150 = $750 USD
- Review: 1 hour × $150 = $150 USD
- **Total**: $900 USD
