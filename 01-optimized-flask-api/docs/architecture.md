# 🏗️ Architecture Documentation

## System Overview

The Secure-SIEM-SOAR-Lab is a comprehensive security operations platform built on a hybrid multi-OS architecture integrating detection (SIEM), response (SOAR), and threat intelligence capabilities.

---

## Architectural Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  Kibana (SIEM UI) | TheHive (Case Mgmt) | Cortex (Responders)   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                              │
│  Fleet Server | Elastic Agent | Python Automation | Webhooks    │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                  │
│  Elasticsearch | Cassandra | MISP Database                      │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    ENDPOINT LAYER                                │
│  Windows Server (Elastic Agent + Sysmon + Windows Firewall API) │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. SIEM Layer (ELK Stack)

#### **Elasticsearch**
- **Role**: Distributed search and analytics engine
- **Function**: 
  - Stores and indexes security logs
  - Performs real-time searches
  - Powers Kibana visualizations
- **Configuration**:
  - Single-node cluster (lab environment)
  - 2GB heap size
  - Security features enabled (TLS, authentication)
- **Data Sources**:
  - Windows Event Logs (Security, System, Application)
  - Sysmon telemetry
  - PowerShell logs

#### **Kibana**
- **Role**: Data visualization and SIEM interface
- **Function**:
  - Security event dashboards
  - Alert management
  - Fleet Server management
  - Detection rule configuration
- **Key Features Used**:
  - Security Solution app
  - Discover (log exploration)
  - Dashboard creation
  - Fleet management

#### **Fleet Server**
- **Role**: Centralized agent management
- **Function**:
  - Agent enrollment
  - Policy distribution
  - Agent monitoring
  - Integration management
- **Configuration**:
  - HTTPS on port 8220
  - Self-signed certificates (lab environment)

#### **Elastic Agent**
- **Role**: Unified data collection agent
- **Deployment**: Windows Server 2022
- **Integrations Enabled**:
  - Windows Event Log
  - Sysmon
  - System metrics
  - Network packet capture (optional)

---

### 2. SOAR Layer (TheHive + Cortex + MISP)

#### **TheHive**
- **Role**: Security incident response platform
- **Function**:
  - Case and alert management
  - Observable tracking (IPs, domains, hashes)
  - Task assignment and workflow
  - Integration with Cortex for automated analysis
- **Data Storage**: Cassandra (NoSQL database)
- **Key Features Used**:
  - Alert creation via webhooks
  - Observable enrichment
  - Responder execution
  - Custom tags and templates

#### **Cortex**
- **Role**: Observable analysis and response orchestration
- **Function**:
  - Execute analyzers on observables (VirusTotal, AbuseIPDB, etc.)
  - Execute responders for automated actions
  - Job management and history
- **Data Storage**: Elasticsearch (same as SIEM)
- **Custom Responders**:
  - WindowsIPBlocker (custom Python responder)

#### **MISP**
- **Role**: Threat intelligence platform
- **Function**:
  - IOC (Indicator of Compromise) storage
  - Threat event correlation
  - Intelligence sharing
  - Feed aggregation
- **Database**: MySQL
- **Integration**: TheHive can query MISP for threat correlation

---

### 3. Custom Automation Layer

#### **WindowsIPBlocker Responder**

**Architecture:**
```
TheHive Observable (IP)
         ↓
    [Cortex executes WindowsIPBlocker.py]
         ↓
    [Python script sends HTTP POST]
         ↓
    [Windows Agent (Flask API on port 5000)]
         ↓
    [netsh command creates firewall rule]
         ↓
    [Windows Firewall blocks IP]
```

**Components:**

1. **WindowsIPBlocker.py** (Ubuntu)
   - Language: Python 3
   - Framework: cortexutils.Responder
   - Function: HTTP client that sends block requests
   - Location: `/opt/Cortex-Analyzers/responders/WindowsIPBlocker/`

2. **windows_agent.py** (Windows)
   - Language: Python 3
   - Framework: Flask (REST API)
   - Function: HTTP server that receives block requests and executes netsh commands
   - Location: `C:\SOC\WindowsBlocker\`
   - Port: 5000
   - Authentication: API key in HTTP header

3. **Communication Flow:**
   ```
   Cortex → HTTP POST → Windows Agent → netsh → Windows Firewall
   
   Request:
   POST http://192.168.106.190:5000/block-ip
   Headers: X-API-Key: <secret>
   Body: {"ip": "192.168.106.200"}
   
   Response:
   {
     "success": true,
     "message": "Successfully blocked IP 192.168.106.200",
     "rule_name": "SOC_Block_192_168_106_200"
   }
   ```

#### **Detection Automation Scripts**

**detect_bruteforce.py:**
- Queries Elasticsearch for Event ID 4625 (failed logins)
- Detects patterns: >5 failures from same IP in 5 minutes
- Can auto-create TheHive alerts

**detect_suspicious_process.py:**
- Queries Elasticsearch for Sysmon Event ID 1 (process creation)
- Detects suspicious patterns:
  - PowerShell with encoded commands
  - Mimikatz-like process names
  - Processes spawned from unusual parents

**get_windows_logs.py:**
- Bulk log retrieval from Elasticsearch
- Exports to CSV for reporting
- Supports custom time ranges and filters

---

## Data Flow Diagrams

### Normal Log Ingestion Flow

```
Windows Server
    │
    ├─ Windows Events (4624, 4625, 4672, etc.)
    ├─ Sysmon Events (1, 3, 7, 8, etc.)
    └─ PowerShell Logs
         │
         ▼
    Elastic Agent
    (collects, filters, enriches)
         │
         ▼ HTTPS (port 8220)
    Fleet Server
    (validates, routes)
         │
         ▼ HTTP (port 9200)
    Elasticsearch
    (indexes, stores)
         │
         ▼ HTTP (port 9200)
    Kibana
    (visualizes, alerts)
```

### Automated Response Flow (Brute Force Attack)

```
Attacker (192.168.106.200)
    │
    ▼ Multiple RDP attempts
Windows Server (192.168.106.190)
    │
    ├─ Logs Event ID 4625 (failed login)
    ▼
Elastic Agent → Fleet Server → Elasticsearch
    │
    ▼ (Webhook configured)
TheHive receives alert
    │
    ├─ Alert: "Brute Force Detected"
    ├─ Observable: IP 192.168.106.200
    │
    ▼ (Analyst runs responder)
Cortex executes WindowsIPBlocker
    │
    ▼ HTTP POST
Windows Agent (port 5000)
    │
    ▼ netsh command
Windows Firewall
    │
    └─ Rule created: SOC_Block_192_168_106_200
    
Result: Attacker IP blocked ✓
```

---

## Network Architecture

### Network Segments

```
┌─────────────────────────────────────────────────────┐
│              NAT Network: 192.168.106.0/24          │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐         ┌──────────────┐         │
│  │ Ubuntu Server│         │Windows Server│         │
│  │  .150        │◄───────►│  .190        │         │
│  │              │         │              │         │
│  │ - ELK Stack  │         │ - Elastic    │         │
│  │ - SOAR Stack │         │   Agent      │         │
│  │ - Docker     │         │ - Sysmon     │         │
│  │              │         │ - Windows    │         │
│  │              │         │   Agent API  │         │
│  └──────────────┘         └──────────────┘         │
│         ▲                         ▲                 │
│         │                         │                 │
│         └────────┬────────────────┘                 │
│                  │                                  │
│         ┌────────▼──────────┐                       │
│         │   Kali Linux      │                       │
│         │   .200            │                       │
│         │                   │                       │
│         │ - Hydra           │                       │
│         │ - Nmap            │                       │
│         │ - Testing tools   │                       │
│         └───────────────────┘                       │
│                                                      │
│                    Gateway: .2                       │
│                    DNS: 8.8.8.8                      │
└─────────────────────────────────────────────────────┘
                      ▲
                      │
                   Internet
```

### Port Matrix (Detailed)

| Service | Host | External Port | Internal Port | Protocol | TLS | Purpose |
|---------|------|---------------|---------------|----------|-----|---------|
| Elasticsearch | Ubuntu | - | 9200 | HTTP | No* | Data storage |
| Elasticsearch Transport | Ubuntu | - | 9300 | TCP | No | Cluster communication |
| Kibana | Ubuntu | 5601 | 5601 | HTTP | No* | SIEM UI |
| Fleet Server | Ubuntu | 8220 | 8220 | HTTPS | Yes | Agent management |
| TheHive | Ubuntu | 9000 | 9000 | HTTP | No | Incident management |
| Cortex | Ubuntu | 9001 | 9001 | HTTP | No | Responder orchestration |
| MISP Web | Ubuntu | 8080 | 80 | HTTP | No | Threat intel web UI |
| MISP HTTPS | Ubuntu | 8443 | 443 | HTTPS | Yes | Threat intel API |
| Windows Agent API | Windows | 5000 | 5000 | HTTP | No | IP blocking endpoint |
| RDP | Windows | 3389 | 3389 | TCP | TLS | Remote desktop |
| SMB | Windows | 445 | 445 | TCP | SMB3 | File sharing |

*\* In production, should be configured with TLS*

---

## Security Architecture

### Authentication & Authorization

#### Elasticsearch/Kibana
- **Auth Method**: Native realm (username/password)
- **Users**:
  - `elastic` (superuser)
  - `kibana_system` (Kibana service account)
- **API Keys**: Used for Fleet Server and integrations

#### TheHive
- **Auth Method**: Local database
- **RBAC**: Organizations, users, profiles
- **API Keys**: For Cortex integration and automation

#### Cortex
- **Auth Method**: Local database
- **RBAC**: Organizations, users, analyzers/responders per org
- **API Keys**: For TheHive callbacks

#### Windows Agent
- **Auth Method**: Custom API key in HTTP header
- **Key**: `X-API-Key: MySOC-2026-SuperSecure-RandomKey-XyZ789`
- **Validation**: Server-side check before executing commands

### Network Security

**Firewall Rules (Ubuntu):**
```bash
# Allow SSH
ufw allow 22/tcp

# Allow Kibana
ufw allow 5601/tcp

# Allow Fleet Server
ufw allow 8220/tcp

# Allow TheHive
ufw allow 9000/tcp

# Allow Cortex
ufw allow 9001/tcp

# Deny all other inbound
ufw default deny incoming
ufw default allow outgoing
```

**Firewall Rules (Windows):**
```powershell
# RDP allowed from 192.168.106.0/24 only
New-NetFirewallRule -DisplayName "RDP - LAN Only" `
  -Direction Inbound -LocalPort 3389 -Protocol TCP `
  -RemoteAddress 192.168.106.0/24 -Action Allow

# Windows Agent API
New-NetFirewallRule -DisplayName "Windows Agent API" `
  -Direction Inbound -LocalPort 5000 -Protocol TCP `
  -RemoteAddress 192.168.106.150 -Action Allow

# Block all other unsolicited inbound
Set-NetFirewallProfile -Profile Domain,Public,Private -DefaultInboundAction Block
```

### Data Protection

**Encryption at Rest:**
- Elasticsearch: Index-level encryption available (not enabled in lab)
- Cassandra: Transparent data encryption available (not enabled in lab)
- MySQL (MISP): InnoDB encryption available (not enabled in lab)

**Encryption in Transit:**
- Fleet Server ↔ Elastic Agent: TLS 1.2+ (self-signed certs in lab)
- MISP: HTTPS with self-signed certificate
- Windows Agent: HTTP (should be HTTPS in production)

---

## Scalability & Performance

### Current Lab Specs

| Component | vCPUs | RAM | Disk | Notes |
|-----------|-------|-----|------|-------|
| Ubuntu Server | 4 | 8GB | 80GB | Runs 7 Docker containers |
| Windows Server | 2 | 4GB | 60GB | Monitored endpoint |
| Kali Linux | 2 | 4GB | 40GB | Attack/testing platform |

### Performance Metrics (Observed)

- **Log ingestion rate**: ~500 events/second
- **Elasticsearch indexing**: ~1000 docs/second
- **Kibana query latency**: <2 seconds for 1M events
- **WindowsIPBlocker response time**: 3-5 seconds (detection → block)
- **TheHive alert creation**: <1 second via webhook

### Scaling Recommendations

**For Production (500-1000 endpoints):**

| Component | vCPUs | RAM | Disk | Notes |
|-----------|-------|-----|------|-------|
| Elasticsearch (3-node cluster) | 8 per node | 32GB per node | 1TB SSD per node | Hot-warm architecture |
| Kibana (2 instances) | 4 per instance | 8GB per instance | 100GB | Load balanced |
| Fleet Server (2 instances) | 4 per instance | 8GB per instance | 100GB | High availability |
| TheHive | 8 | 16GB | 500GB | Cassandra cluster (3 nodes) |
| Cortex | 4 | 8GB | 200GB | Dedicated worker nodes |

---

## Disaster Recovery

### Backup Strategy

**Daily Backups:**
- Elasticsearch snapshots → S3/NFS
- Cassandra snapshots → S3/NFS
- MISP database dump → S3/NFS
- Docker volume backups

**Configuration Backups:**
- All `.yml`, `.conf` files → Git repository
- Kibana saved objects → ndjson export
- TheHive case templates → JSON export
- Cortex responder configurations → JSON export

### Recovery Procedures

**Elasticsearch Recovery:**
```bash
# Restore from snapshot
curl -X POST "localhost:9200/_snapshot/my_backup/snapshot_1/_restore"
```

**TheHive Recovery:**
```bash
# Stop TheHive
docker-compose stop thehive

# Restore Cassandra backup
# ... (specific to Cassandra backup tool used)

# Restart TheHive
docker-compose start thehive
```

---

## Monitoring & Alerting

### System Monitoring

**Docker Containers:**
```bash
# Monitor container health
docker ps
docker stats

# Check logs
docker logs elasticsearch --tail 100 -f
docker logs cortex --tail 100 -f
```

**Elasticsearch Cluster Health:**
```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
curl -X GET "localhost:9200/_cat/indices?v"
```

### Security Monitoring

**Key Metrics to Monitor:**
- Failed login attempts (Event ID 4625) > threshold
- New service installations (Event ID 7045)
- PowerShell execution with obfuscation
- Unusual network connections
- Privilege escalation events (Event ID 4672)

**Alert Channels:**
- Slack webhooks (critical alerts)
- Email (daily digest)
- TheHive case creation (automated triage)
- Jira ticket creation (for IT coordination)

---

## Future Enhancements

### Planned Improvements

1. **Machine Learning Integration**
   - Elastic ML for anomaly detection
   - Behavioral analysis of user activity

2. **Additional Responders**
   - DNS sinkholing
   - Email quarantine
   - Active Directory account lockout

3. **Extended Threat Intelligence**
   - Additional MISP feeds
   - Commercial threat intel integrations

4. **Kubernetes Deployment**
   - Container orchestration
   - Auto-scaling
   - Improved resilience

---

## Appendix: Technology Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **SIEM** | Elasticsearch | 8.11.0 | Log storage & search |
| | Kibana | 8.11.0 | Visualization |
| | Fleet Server | 8.11.0 | Agent management |
| | Elastic Agent | 8.11.0 | Data collection |
| **SOAR** | TheHive | 5.2 | Incident response |
| | Cortex | 3.1 | Response automation |
| | MISP | 2.4 | Threat intelligence |
| **Database** | Cassandra | 4.0 | TheHive storage |
| | MySQL | 5.7 | MISP storage |
| **Container** | Docker | 24.0+ | Containerization |
| | Docker Compose | 2.20+ | Orchestration |
| **OS** | Ubuntu Server | 22.04 LTS | SIEM/SOAR host |
| | Windows Server | 2022 | Monitored endpoint |
| | Kali Linux | 2024.1 | Testing platform |
| **Language** | Python | 3.11 | Automation scripts |
| | Bash | 5.1 | Shell scripts |
| | PowerShell | 5.1 | Windows automation |
| **Telemetry** | Sysmon | 15.0 | Enhanced Windows logs |

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Author**: Mahamadou DANSOKO