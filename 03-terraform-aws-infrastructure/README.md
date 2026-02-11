# ☁️ Terraform AWS Infrastructure - Infrastructure as Code

Provision complete AWS infrastructure using Terraform: VPC, subnets, security groups, EC2, EKS, RDS, and more.

**Part of:** [DevOps Learning Journey](../README.md)  
**Status:** ⏳ Coming Soon (Week 7-9)  
**Prerequisites:** [01-optimized-flask-api](../01-optimized-flask-api), [02-kubernetes-deployment](../02-kubernetes-deployment)

---

## 🎯 Learning Objectives

- [ ] Master Terraform basics (providers, resources, state)
- [ ] Learn HCL (HashiCorp Configuration Language) syntax
- [ ] Provision AWS VPC with public/private subnets
- [ ] Deploy EC2 instances with security groups
- [ ] Create RDS PostgreSQL database
- [ ] Provision EKS (Elastic Kubernetes Service) cluster
- [ ] Manage Terraform state remotely (S3 + DynamoDB)
- [ ] Create reusable Terraform modules
- [ ] Implement workspaces (dev/staging/prod)
- [ ] Generate infrastructure diagrams

---

## 🏗️ What We'll Build

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Cloud                             │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              VPC (10.0.0.0/16)                         │ │
│  │                                                        │ │
│  │  ┌──────────────────────┐  ┌──────────────────────┐  │ │
│  │  │  Public Subnet       │  │  Private Subnet      │  │ │
│  │  │  10.0.1.0/24         │  │  10.0.10.0/24        │  │ │
│  │  │                      │  │                      │  │ │
│  │  │  ┌────────────┐      │  │  ┌────────────┐     │  │ │
│  │  │  │   Bastion  │      │  │  │    EKS     │     │  │ │
│  │  │  │    Host    │      │  │  │   Nodes    │     │  │ │
│  │  │  └────────────┘      │  │  └────────────┘     │  │ │
│  │  │                      │  │                      │  │ │
│  │  │  ┌────────────┐      │  │  ┌────────────┐     │  │ │
│  │  │  │    ALB     │      │  │  │    RDS     │     │  │ │
│  │  │  │(Load Bal.) │      │  │  │ PostgreSQL │     │  │ │
│  │  │  └────────────┘      │  │  └────────────┘     │  │ │
│  │  └──────────────────────┘  └──────────────────────┘  │ │
│  │           │                          │                │ │
│  │           └──────────┬───────────────┘                │ │
│  │                      │                                │ │
│  │              ┌───────▼────────┐                       │ │
│  │              │  NAT Gateway   │                       │ │
│  │              └────────────────┘                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Terraform State Backend                   │ │
│  │  ┌──────────────┐      ┌──────────────┐               │ │
│  │  │  S3 Bucket   │      │  DynamoDB    │               │ │
│  │  │(State files) │      │(State lock)  │               │ │
│  │  └──────────────┘      └──────────────┘               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Components

1. **Networking**
   - VPC with CIDR block
   - Public and private subnets across 2 AZs
   - Internet Gateway
   - NAT Gateway
   - Route tables

2. **Compute**
   - EC2 bastion host (jump server)
   - EKS cluster with worker nodes
   - Auto Scaling Groups

3. **Database**
   - RDS PostgreSQL instance
   - Multi-AZ deployment (optional)
   - Automated backups

4. **Load Balancing**
   - Application Load Balancer (ALB)
   - Target groups
   - Health checks

5. **Security**
   - Security groups (least privilege)
   - IAM roles and policies
   - KMS encryption keys

6. **Storage**
   - S3 buckets (app data, Terraform state)
   - EBS volumes

7. **Monitoring**
   - CloudWatch alarms
   - SNS notifications

---

## 📋 Project Structure (Preview)
```
03-terraform-aws-infrastructure/
├── README.md
├── main.tf                  # Main configuration
├── variables.tf             # Input variables
├── outputs.tf               # Output values
├── terraform.tfvars         # Variable values (gitignored)
├── versions.tf              # Provider versions
├── backend.tf               # Remote state config
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── security/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       └── terraform.tfvars
├── scripts/
│   ├── init.sh
│   ├── plan.sh
│   ├── apply.sh
│   └── destroy.sh
└── docs/
    ├── architecture-diagram.png
    └── cost-estimation.md
```

---

## 🛠️ Technologies

- **Terraform:** v1.6+
- **AWS CLI:** v2.x
- **Cloud Provider:** AWS
- **State Backend:** S3 + DynamoDB
- **Visualization:** Terraform Graph, Graphviz

---

## 🚀 Quick Start (Coming Soon)
```bash
# Configure AWS credentials
aws configure

# Initialize Terraform
terraform init

# Plan infrastructure
terraform plan

# Apply changes
terraform apply

# Generate graph
terraform graph | dot -Tpng > graph.png

# Destroy (when done)
terraform destroy
```

---

## 💰 Cost Estimation

| Resource | Monthly Cost (Estimated) |
|----------|--------------------------|
| VPC & Networking | $30-50 |
| EKS Cluster | $72 |
| EC2 (t3.medium x 3) | $90 |
| RDS (db.t3.micro) | $15 |
| NAT Gateway | $32 |
| **Total** | **~$240/month** |

**Note:** Use `terraform destroy` after learning to avoid charges!

---

## 📈 Success Metrics

- [ ] VPC created with proper CIDR blocks
- [ ] EKS cluster accessible via kubectl
- [ ] RDS instance reachable from private subnet
- [ ] ALB distributing traffic to EC2 instances
- [ ] Terraform state stored in S3 with locking
- [ ] Infrastructure diagram generated
- [ ] Multi-environment setup working (dev/staging/prod)

---

## 📚 Resources

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

**⬅️ [Previous: Kubernetes](../02-kubernetes-deployment) | [Next: CI/CD Pipeline →](../04-cicd-github-actions)**