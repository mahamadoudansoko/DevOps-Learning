# 🏗️ Kubernetes Architecture

## Overview
```
Internet
    │
    ▼
┌─────────────────────────────────────┐
│         Minikube Cluster            │
│                                     │
│  ┌─────────┐                        │
│  │ Ingress │ flask-api.local        │
│  │  NGINX  │                        │
│  └────┬────┘                        │
│       │                             │
│  ┌────▼─────────────────────────┐   │
│  │        flask-app namespace   │   │
│  │                              │   │
│  │  ┌────────┐ ┌────────┐ ┌──────┐ │
│  │  │ Flask  │ │ Flask  │ │Flask │ │
│  │  │  Pod   │ │  Pod   │ │ Pod  │ │
│  │  └────────┘ └────────┘ └──────┘ │
│  │       │                         │
│  │  ┌────▼──────┐                  │
│  │  │ PostgreSQL│                  │
│  │  │   Pod     │                  │
│  │  └────┬──────┘                  │
│  │       │                         │
│  │  ┌────▼──────┐                  │
│  │  │    PVC    │ 1Gi Storage      │
│  │  └───────────┘                  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Components

### Namespace
- `flask-app` — isolates all resources

### Flask API Deployment
- 3 replicas (dev: 1, prod: 5)
- Rolling update strategy (zero downtime)
- Resource limits: CPU 500m, Memory 512Mi
- Health checks: `/health`, `/ready`

### PostgreSQL StatefulSet
- 1 replica
- Persistent storage via PVC (1Gi)
- Headless service for stable DNS

### Ingress NGINX
- Host: `flask-api.local`
- Routes all traffic to flask-service
- Accessible via minikube tunnel

### HPA (Horizontal Pod Autoscaler)
- Min replicas: 2
- Max replicas: 10
- Scale up: CPU > 70%, Memory > 80%

### ConfigMap & Secrets
- ConfigMap: app environment variables
- Secret: API keys, DB credentials

## Environments

| Setting | Dev | Prod |
|---------|-----|------|
| Replicas | 1 | 5 |
| CPU request | 50m | 200m |
| Memory request | 64Mi | 256Mi |
| Max replicas | 3 | 20 |
| Storage | 512Mi | 10Gi |

## Helm Chart
```bash
# Deploy dev
helm install flask-app ./helm/flask-app --values helm/flask-app/values-dev.yaml -n flask-app

# Deploy prod
helm install flask-app ./helm/flask-app --values helm/flask-app/values-prod.yaml -n flask-app

# Upgrade
helm upgrade flask-app ./helm/flask-app --values helm/flask-app/values-dev.yaml -n flask-app

# Uninstall
helm uninstall flask-app -n flask-app
```