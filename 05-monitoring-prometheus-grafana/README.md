# 📊 Monitoring & Observability - Prometheus, Grafana & ELK

Complete observability stack with metrics (Prometheus), visualization (Grafana), logs (ELK), and tracing (Jaeger).

**Part of:** [DevOps Learning Journey](../README.md)  
**Status:** ⏳ Coming Soon (Week 12)  
**Prerequisites:** All previous projects

---

## 🎯 Learning Objectives

- [ ] Understand observability (metrics, logs, traces)
- [ ] Deploy Prometheus for metrics collection
- [ ] Create Grafana dashboards
- [ ] Implement ELK Stack for log aggregation
- [ ] Set up distributed tracing with Jaeger
- [ ] Configure alerting (Alertmanager, PagerDuty)
- [ ] Write PromQL queries
- [ ] Create custom exporters
- [ ] Implement SLO/SLI monitoring
- [ ] Set up on-call rotation

---

## 🏗️ What We'll Build

### The Three Pillars of Observability
```
┌─────────────────────────────────────────────────────────────┐
│                    Application (Flask API)                   │
└──────┬─────────────────┬────────────────────┬───────────────┘
       │                 │                    │
       │ Metrics         │ Logs               │ Traces
       │                 │                    │
       ▼                 ▼                    ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Prometheus  │   │     ELK     │   │   Jaeger    │
│             │   │             │   │             │
│ - CPU/RAM   │   │ - App logs  │   │ - Req/Resp  │
│ - Requests  │   │ - Access    │   │ - Latency   │
│ - Errors    │   │ - Errors    │   │ - Deps      │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                    │
       │                 │                    │
       ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                       Grafana                                │
│                 (Unified Dashboard)                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Metrics    │  │     Logs     │  │    Traces    │      │
│  │  Dashboard   │  │   Dashboard  │  │   Dashboard  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                     Alertmanager                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Slack     │  │  PagerDuty   │  │    Email     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Monitoring Stack Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Monitoring Namespace                       │ │
│  │                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │ Prometheus  │  │   Grafana   │  │Alertmanager │   │ │
│  │  │   Server    │  │             │  │             │   │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │ │
│  │         │                │                │           │ │
│  │         │   ┌────────────┴────────────┐   │           │ │
│  │         │   │                         │   │           │ │
│  └─────────┼───┼─────────────────────────┼───┼───────────┘ │
│            │   │                         │   │             │
│  ┌─────────▼───▼──────────────────┐      │   │             │
│  │      Application Namespace      │      │   │             │
│  │                                 │      │   │             │
│  │  ┌──────────┐  ┌──────────┐    │      │   │             │
│  │  │  Flask   │  │  Flask   │    │      │   │             │
│  │  │  Pod 1   │  │  Pod 2   │    │◄─────┘   │             │
│  │  │          │  │          │    │          │             │
│  │  │ /metrics │  │ /metrics │    │          │             │
│  │  └──────────┘  └──────────┘    │          │             │
│  └─────────────────────────────────┘          │             │
│                                                │             │
│  ┌─────────────────────────────────────────┐  │             │
│  │         Logging Namespace                │  │             │
│  │                                          │  │             │
│  │  ┌──────────┐  ┌──────────┐  ┌────────┐│  │             │
│  │  │Fluent Bit│  │Elastics- │  │ Kibana ││  │             │
│  │  │(Agent)   │─>│  earch   │─>│        ││  │             │
│  │  └──────────┘  └──────────┘  └────────┘│  │             │
│  └─────────────────────────────────────────┘  │             │
│                                                │             │
│  ┌─────────────────────────────────────────┐  │             │
│  │        Tracing Namespace                 │  │             │
│  │                                          │  │             │
│  │  ┌──────────┐  ┌──────────┐  ┌────────┐│  │             │
│  │  │  Jaeger  │  │  Jaeger  │  │Jaeger  ││  │             │
│  │  │  Agent   │─>│Collector │─>│  UI    ││  │             │
│  │  └──────────┘  └──────────┘  └────────┘│  │             │
│  └─────────────────────────────────────────┘  │             │
│                                                │             │
└────────────────────────────────────────────────┼─────────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │  Alerting       │
                                        │  (Slack/Email)  │
                                        └─────────────────┘
```

---

## 📋 Project Structure (Preview)
```
05-monitoring-prometheus-grafana/
├── README.md
├── prometheus/
│   ├── prometheus.yml           # Config
│   ├── alerts.yml               # Alert rules
│   └── recording-rules.yml      # Recording rules
├── grafana/
│   ├── dashboards/
│   │   ├── flask-api.json
│   │   ├── kubernetes.json
│   │   └── slo-dashboard.json
│   ├── datasources/
│   │   ├── prometheus.yaml
│   │   ├── elasticsearch.yaml
│   │   └── jaeger.yaml
│   └── provisioning/
│       └── dashboards.yaml
├── elk/
│   ├── elasticsearch.yml
│   ├── logstash.conf
│   └── filebeat.yml
├── jaeger/
│   └── jaeger-all-in-one.yaml
├── alertmanager/
│   ├── alertmanager.yml
│   └── templates/
│       └── slack.tmpl
├── k8s/
│   ├── prometheus-deployment.yaml
│   ├── grafana-deployment.yaml
│   ├── elk-stack.yaml
│   └── jaeger-deployment.yaml
├── exporters/
│   └── custom-flask-exporter.py
└── docs/
    ├── metrics-guide.md
    ├── dashboard-screenshots/
    └── alerting-playbook.md
```

---

## 🛠️ Technologies

### Metrics
- **Prometheus** - Metrics collection & storage
- **Grafana** - Visualization
- **Alertmanager** - Alert routing & silencing
- **Node Exporter** - System metrics
- **cAdvisor** - Container metrics
- **Blackbox Exporter** - Endpoint monitoring

### Logging
- **Elasticsearch** - Log storage & search
- **Logstash** - Log processing
- **Kibana** - Log visualization
- **Fluent Bit** - Log collection (lightweight)

### Tracing
- **Jaeger** - Distributed tracing
- **OpenTelemetry** - Instrumentation

### Alerting
- **Alertmanager** - Alert management
- **Slack** - Notifications
- **PagerDuty** - On-call management

---

## 🚀 Quick Start (Coming Soon)
```bash
# Deploy Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack

# Deploy Grafana (included in above)

# Deploy ELK Stack
helm install elasticsearch elastic/elasticsearch
helm install kibana elastic/kibana

# Deploy Jaeger
kubectl apply -f jaeger/jaeger-all-in-one.yaml

# Access Grafana
kubectl port-forward svc/prometheus-grafana 3000:80

# Access Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090

# Access Kibana
kubectl port-forward svc/kibana 5601:5601
```

---

## 📊 Dashboards & Alerts

### Grafana Dashboards

1. **Flask API Performance**
   - Request rate
   - Response time (p50, p95, p99)
   - Error rate
   - Active connections

2. **Kubernetes Cluster**
   - Node CPU/Memory
   - Pod status
   - Network I/O
   - Storage usage

3. **SLO Dashboard**
   - Availability (uptime %)
   - Latency SLI
   - Error budget
   - Burn rate

### Prometheus Alerts
```yaml
# Example: High Error Rate
- alert: HighErrorRate
  expr: rate(flask_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate detected"
    description: "Error rate is {{ $value }} errors/sec"
```

---

## 📈 Success Metrics

- [ ] Prometheus scraping all targets
- [ ] Grafana dashboards showing real-time data
- [ ] Logs aggregated in Elasticsearch
- [ ] Distributed traces visible in Jaeger
- [ ] Alerts firing and routing correctly
- [ ] SLO dashboard tracking 99.9% uptime
- [ ] Custom exporters working
- [ ] On-call rotation configured

---

## 📚 Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [Elastic Stack Guide](https://www.elastic.co/guide/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [SRE Book (Google)](https://sre.google/books/)

---

**⬅️ [Previous: CI/CD Pipeline](../04-cicd-github-actions) | 🎉 Journey Complete!**