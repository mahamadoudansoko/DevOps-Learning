# 🚀 DevOps & DevSecOps Learning Journey

A comprehensive, hands-on learning path for mastering DevOps and DevSecOps practices through real-world projects.

**Author:** Mahamadou DANSOKO  
**Duration:** 12-14 weeks  
**Goal:** Build production-ready DevOps/DevSecOps portfolio

---

## 📚 Learning Roadmap

| Phase | Duration | Status | Projects |
|-------|----------|--------|----------|
| **Phase 1: Docker & Containers** | 3 weeks | ✅ Complete | [01-optimized-flask-api](#01-optimized-flask-api) |
| **Phase 2: Kubernetes** | 3 weeks | 🔄 In Progress | [02-kubernetes-deployment](#02-kubernetes-deployment) |
| **Phase 3: Infrastructure as Code** | 3 weeks | ⏳ Planned | [03-terraform-aws-infrastructure](#03-terraform-aws-infrastructure) |
| **Phase 4: CI/CD Pipelines** | 2 weeks | ⏳ Planned | [04-jenkins-cicd-pipeline](#04-jenkins-cicd-pipeline) |
| **Phase 5: Monitoring & Observability** | 1 week | ⏳ Planned | [05-monitoring-prometheus-grafana](#05-monitoring-prometheus-grafana) |

---

## 🎯 Projects Overview

### 01-optimized-flask-api
**Status:** ✅ Complete  
**Technologies:** Docker, Flask, Python, Multi-stage builds, Alpine Linux  
**Description:** Production-ready Flask API with optimized Docker container (< 80MB), security best practices, and comprehensive testing.

**Key Features:**
- Multi-stage Docker build
- Non-root user execution
- API key authentication
- Health & readiness probes
- Structured JSON logging
- Security headers (XSS, CSRF protection)
- Unit tests with pytest

**Metrics:**
- Image size: ~75MB (vs 500MB+ standard Python image)
- Build time: ~90 seconds
- Startup time: <3 seconds
- Test coverage: 100%

[📂 View Project →](./01-optimized-flask-api)

---

### 02-kubernetes-deployment
**Status:** ⏳ Coming Soon  
**Technologies:** Kubernetes, kubectl, Helm, Minikube/k3s  
**Description:** Deploy microservices to Kubernetes with auto-scaling, ingress, and persistent storage.

[📂 View Project →](./02-kubernetes-deployment)

---

### 03-terraform-aws-infrastructure
**Status:** ⏳ Coming Soon  
**Technologies:** Terraform, AWS, VPC, EC2, EKS, RDS  
**Description:** Provision complete AWS infrastructure as code with Terraform modules.

[📂 View Project →](./03-terraform-aws-infrastructure)

---

### 04-jenkins-cicd-pipeline
**Status:** ⏳ Coming Soon  
**Technologies:** Jenkins, GitHub Actions, GitLab CI  
**Description:** Automated CI/CD pipeline with testing, security scanning, and deployment.

[📂 View Project →](./04-jenkins-cicd-pipeline)

---

### 05-monitoring-prometheus-grafana
**Status:** ⏳ Coming Soon  
**Technologies:** Prometheus, Grafana, ELK Stack, Jaeger  
**Description:** Complete observability stack with metrics, logs, and distributed tracing.

[📂 View Project →](./05-monitoring-prometheus-grafana)

---

## 🛠️ Tech Stack

### Containerization & Orchestration
- Docker & Docker Compose
- Kubernetes (kubectl, Helm)
- Container registries (Docker Hub, AWS ECR)

### Infrastructure as Code
- Terraform
- Ansible
- CloudFormation (AWS)

### CI/CD
- GitHub Actions
- Jenkins
- GitLab CI/CD

### Programming & Scripting
- Python (Flask, FastAPI)
- Bash scripting
- PowerShell

### Cloud Providers
- AWS (primary)
- Azure (secondary)

### Monitoring & Logging
- Prometheus
- Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Jaeger (distributed tracing)

### Security
- Trivy (container scanning)
- SonarQube (SAST)
- OWASP ZAP (DAST)
- HashiCorp Vault (secrets management)

---

## 📈 Learning Progress
```
Week 1-3:   Docker Mastery ████████████████████ 100%
Week 4-6:   Kubernetes      ░░░░░░░░░░░░░░░░░░░░   0%
Week 7-9:   IaC (Terraform) ░░░░░░░░░░░░░░░░░░░░   0%
Week 10-11: DevSecOps       ░░░░░░░░░░░░░░░░░░░░   0%
Week 12:    Monitoring      ░░░░░░░░░░░░░░░░░░░░   0%
```

---

## 🎓 Skills Acquired

### Completed ✅
- [x] Multi-stage Docker builds
- [x] Container security best practices
- [x] Python application containerization
- [x] Docker networking
- [x] Health checks & readiness probes
- [x] API development (Flask)
- [x] Unit testing with pytest
- [x] Security scanning (Trivy)

### In Progress 🔄
- [ ] Kubernetes deployment
- [ ] Helm charts
- [ ] Horizontal Pod Autoscaling

### Upcoming ⏳
- [ ] Terraform modules
- [ ] CI/CD pipelines
- [ ] Prometheus metrics
- [ ] Grafana dashboards

---

## 📚 Resources

### Documentation
- [Docker Official Docs](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform Tutorials](https://learn.hashicorp.com/terraform)

### Learning Platforms
- [TryHackMe DevOps Path](https://tryhackme.com/)
- [KodeKloud](https://kodekloud.com/)
- [A Cloud Guru](https://acloudguru.com/)

### Books
- "The DevOps Handbook" - Gene Kim
- "Kubernetes in Action" - Marko Lukša
- "Terraform: Up & Running" - Yevgeniy Brikman

---

## 🤝 Connect

**Mahamadou DANSOKO**
- 🔗 LinkedIn: [linkedin.com/in/tjodansoko](https://linkedin.com/in/tjodoudansoko)
- 🐙 GitHub: [github.com/mahamadoudansoko](https://github.com/mahamadoudansoko)
- 📧 Email: dansokomaha@gmail.com

---

## 📄 License

This repository is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If you find this learning journey helpful, please consider:
- ⭐ Starring this repository
- 🔄 Forking it for your own learning
- 📢 Sharing it with others

---

**Last Updated:** February 2026  
**Next Milestone:** Kubernetes deployment complete by Week 6