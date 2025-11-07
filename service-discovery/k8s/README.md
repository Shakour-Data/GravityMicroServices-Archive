# Kubernetes Deployment Guide

## Prerequisites

- Kubernetes cluster (v1.28+)
- kubectl configured
- Namespace `gravity` created
- PostgreSQL and Redis deployed (or use external services)
- Consul deployed (or use external service)

## Quick Start

### 1. Create Namespace

```bash
kubectl create namespace gravity
```

### 2. Update Secrets

Edit `secret.yaml` and update the credentials:
- DATABASE_URL
- REDIS_URL
- SECRET_KEY

### 3. Deploy

```bash
# Deploy in order
kubectl apply -f rbac.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
kubectl apply -f ingress.yaml
```

Or deploy all at once:

```bash
kubectl apply -f k8s/
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n gravity

# Check services
kubectl get svc -n gravity

# Check logs
kubectl logs -f deployment/service-discovery -n gravity
```

## Scaling

The deployment uses HorizontalPodAutoscaler (HPA):
- Min replicas: 3
- Max replicas: 10
- CPU threshold: 70%
- Memory threshold: 80%

Manual scaling:
```bash
kubectl scale deployment service-discovery -n gravity --replicas=5
```

## Monitoring

Access metrics:
```bash
kubectl port-forward svc/service-discovery 9090:9090 -n gravity
# Visit http://localhost:9090/metrics
```

## Troubleshooting

### Pods not starting

```bash
kubectl describe pod <pod-name> -n gravity
kubectl logs <pod-name> -n gravity
```

### Database connection issues

```bash
# Check secret
kubectl get secret service-discovery-secrets -n gravity -o yaml

# Test database connection
kubectl run -it --rm debug --image=postgres:16 --restart=Never -n gravity -- psql <DATABASE_URL>
```

### Rolling update

```bash
kubectl rollout status deployment/service-discovery -n gravity
kubectl rollout history deployment/service-discovery -n gravity
kubectl rollout undo deployment/service-discovery -n gravity
```

## Cleanup

```bash
kubectl delete -f k8s/
```
