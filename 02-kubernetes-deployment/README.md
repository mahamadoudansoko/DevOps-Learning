# ⚓ Kubernetes Deployment - Microservices Orchestration

Deploy the Flask API to Kubernetes with auto-scaling, ingress, persistent storage, and service mesh.

**Part of:** [DevOps Learning Journey](../README.md)  
**Status:** ⏳ Coming Soon (Week 4-6)  
**Prerequisites:** Completion of [01-optimized-flask-api](../01-optimized-flask-api)

---

## 🎯 Learning Objectives

- [ ] Understand Kubernetes architecture (pods, nodes, clusters)
- [ ] Master kubectl commands and YAML manifests
- [ ] Deploy multi-container applications
- [ ] Configure ConfigMaps and Secrets
- [ ] Implement Horizontal Pod Autoscaling (HPA)
- [ ] Set up Ingress controllers (NGINX)
- [ ] Manage persistent volumes (PV/PVC)
- [ ] Create and publish Helm charts
- [ ] Implement service mesh basics (optional)

---

## 🏗️ What We'll Build

### Architecture
```
                     Internet
                        │
                        ▼
                   ┌─────────┐
                   │ Ingress │
                   │ (NGINX) │
                   └────┬────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │  Flask  │    │  Flask  │    │  Flask  │
   │   Pod   │    │   Pod   │    │   Pod   │
   │ (App 1) │    │ (App 2) │    │ (App 3) │
   └────┬────┘    └────┬────┘    └────┬────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                        ▼
                  ┌──────────┐
                  │PostgreSQL│
                  │   Pod    │
                  │   (PVC)  │
                  └──────────┘
```

### Components

1. **Deployment Manifests**
   - Flask API deployment (3 replicas)
   - PostgreSQL StatefulSet
   - Redis deployment

2. **Services**
   - ClusterIP for internal communication
   - LoadBalancer for external access

3. **ConfigMaps & Secrets**
   - Application configuration
   - Database credentials
   - API keys

4. **Ingress**
   - NGINX Ingress Controller
   - TLS/SSL termination
   - Path-based routing

5. **Autoscaling**
   - Horizontal Pod Autoscaler (HPA)
   - CPU/Memory-based scaling
   - Custom metrics (optional)

6. **Persistent Storage**
   - PersistentVolume for PostgreSQL
   - PersistentVolumeClaim
   - Storage classes

7. **Helm Chart**
   - Templated manifests
   - values.yaml for environments
   - Chart dependencies

---

## 📋 Project Structure (Preview)
```
02-kubernetes-deployment/
├── README.md
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── flask-deployment.yaml
│   ├── flask-service.yaml
│   ├── postgres-statefulset.yaml
│   ├── postgres-pvc.yaml
│   ├── redis-deployment.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
├── helm/
│   └── flask-microservices/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-prod.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── ingress.yaml
│           └── hpa.yaml
├── scripts/
│   ├── deploy.sh
│   ├── scale.sh
│   └── cleanup.sh
└── docs/
    └── kubernetes-concepts.md
```

---

## 🛠️ Technologies

- **Kubernetes:** v1.28+
- **kubectl:** Latest
- **Helm:** v3.12+
- **Local Cluster:** Minikube / k3s / Kind
- **Ingress:** NGINX Ingress Controller
- **Storage:** Local or cloud-based PV

---

## 🚀 Quick Start (Coming Soon)
```bash
# Install minikube
# TBD

# Deploy application
kubectl apply -f k8s/

# Or using Helm
helm install flask-app helm/flask-microservices

# Access the application
kubectl port-forward svc/flask-api 5000:5000
```

---

## 📈 Success Metrics

- [ ] Application runs with 3 replicas
- [ ] Auto-scaling triggers on CPU > 70%
- [ ] Zero-downtime rolling updates
- [ ] Persistent data survives pod restarts
- [ ] Ingress accessible from browser
- [ ] Helm chart published to repository

---

## 📚 Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [KodeKloud Kubernetes Course](https://kodekloud.com/courses/kubernetes-for-beginners/)

---

**⬅️ [Previous: Docker Optimization](../01-optimized-flask-api) | [Next: Terraform IaC →](../03-terraform-aws-infrastructure)**