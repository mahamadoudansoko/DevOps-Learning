# ☁️ Terraform AWS Infrastructure (LocalStack) - Infrastructure as Code

Provision complete AWS infrastructure using Terraform locally with LocalStack: VPC, subnets, security groups, EC2, RDS, and more — no AWS account or credit card required.

**Part of:** [DevOps Learning Journey](../README.md)
**Status:** 🚧 In Progress (Week 7-9)
**Prerequisites:** [01-optimized-flask-api](../01-optimized-flask-api), [02-kubernetes-deployment](../02-kubernetes-deployment)

---

## ⚠️ LocalStack Notice

This project uses **LocalStack** to simulate AWS services locally. This means:
- ✅ No AWS account needed
- ✅ No credit card required
- ✅ Completely free
- ⚠️ EKS simulation is limited — worker node behavior differs from real AWS
- ⚠️ Some advanced features (KMS, Multi-AZ RDS) may behave differently

When you're ready for a real AWS deployment, the Terraform code here is fully transferable — just swap the provider config.

---

## 🎯 Learning Objectives

- [ ] Master Terraform basics (providers, resources, state)
- [ ] Learn HCL (HashiCorp Configuration Language) syntax
- [ ] Provision AWS VPC with public/private subnets
- [ ] Deploy EC2 instances with security groups
- [ ] Create RDS PostgreSQL database
- [ ] Provision EKS (Elastic Kubernetes Service) cluster
- [ ] Manage Terraform state locally (local backend) and understand remote state (S3 + DynamoDB)
- [ ] Create reusable Terraform modules
- [ ] Implement workspaces (dev/staging/prod)
- [ ] Generate infrastructure diagrams

---

## 🏗️ What We'll Build

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                   LocalStack (local AWS sim)                 │
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
│  │  │  │    Host    │      │  │  │  (simulated)│     │  │ │
│  │  │  └────────────┘      │  │  └────────────┘     │  │ │
│  │  │                      │  │                      │  │ │
│  │  │  ┌────────────┐      │  │  ┌────────────┐     │  │ │
│  │  │  │    ALB     │      │  │  │    RDS     │     │  │ │
│  │  │  │(simulated) │      │  │  │ PostgreSQL │     │  │ │
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
│  │              Terraform State (local backend)           │ │
│  │  ┌──────────────┐      ┌──────────────┐               │ │
│  │  │ terraform    │      │  S3 bucket   │               │ │
│  │  │ .tfstate     │      │ (LocalStack) │               │ │
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
   - EKS cluster with worker nodes (simulated)
   - Auto Scaling Groups

3. **Database**
   - RDS PostgreSQL instance
   - Automated backups (simulated)

4. **Load Balancing**
   - Application Load Balancer (ALB)
   - Target groups
   - Health checks

5. **Security**
   - Security groups (least privilege)
   - IAM roles and policies

6. **Storage**
   - S3 buckets (app data, Terraform state)
   - EBS volumes

7. **Monitoring**
   - CloudWatch alarms (simulated)
   - SNS notifications (simulated)

---

## 📋 Project Structure
```
03-terraform-aws-infrastructure/
├── README.md
├── main.tf                  # Main configuration
├── variables.tf             # Input variables
├── outputs.tf               # Output values
├── terraform.tfvars         # Variable values (gitignored)
├── versions.tf              # Provider versions
├── backend.tf               # Local state config (swap for S3 on real AWS)
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
    └── localstack-limitations.md
```

---

## 🛠️ Technologies

- **Terraform:** v1.6+
- **LocalStack:** v3.x (free tier)
- **awslocal CLI:** Latest (wrapper around AWS CLI for LocalStack)
- **Docker:** Required to run LocalStack
- **Visualization:** Terraform Graph, Graphviz

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
# Install LocalStack (requires Docker running)
pip install localstack

# Install the LocalStack AWS CLI wrapper
pip install awscli-local

# Install Terraform
# https://developer.hashicorp.com/terraform/install
```

### 2. Start LocalStack

```bash
# Start LocalStack in the background
localstack start -d

# Verify it's running
localstack status services
```

### 3. Configure the Terraform provider for LocalStack

In `versions.tf` or `main.tf`, use this provider block instead of real AWS credentials:

```hcl
provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  region                      = "us-east-1"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    ec2      = "http://localhost:4566"
    s3       = "http://localhost:4566"
    rds      = "http://localhost:4566"
    eks      = "http://localhost:4566"
    iam      = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
    elb      = "http://localhost:4566"
    elbv2    = "http://localhost:4566"
    cloudwatch = "http://localhost:4566"
    sns      = "http://localhost:4566"
  }
}
```

### 4. Deploy

```bash
# Initialize Terraform
terraform init

# Preview infrastructure
terraform plan

# Apply
terraform apply

# Generate graph (requires Graphviz)
terraform graph | dot -Tpng > docs/architecture-diagram.png

# Tear down
terraform destroy
```

### 5. Inspect resources with awslocal

```bash
# List S3 buckets
awslocal s3 ls

# List VPCs
awslocal ec2 describe-vpcs

# List RDS instances
awslocal rds describe-db-instances
```

---

## 💰 Cost

**$0.00** — LocalStack runs entirely on your machine inside Docker.

---

## ⚡ LocalStack Service Support

| Service | Support Level |
|---------|--------------|
| VPC / Subnets / Route Tables | ✅ Full |
| EC2 | ✅ Full |
| S3 | ✅ Full |
| IAM | ✅ Full |
| RDS PostgreSQL | ✅ Good |
| ALB / ELB | ✅ Good |
| DynamoDB | ✅ Full |
| CloudWatch | ⚠️ Partial |
| EKS | ⚠️ Limited |
| KMS | ⚠️ Limited |
| NAT Gateway | ⚠️ Simulated only |

---

## 📈 Success Metrics

- [ ] LocalStack running and healthy
- [ ] VPC created with proper CIDR blocks
- [ ] RDS instance reachable from private subnet
- [ ] ALB distributing traffic to EC2 instances
- [ ] Terraform state stored in local backend
- [ ] Infrastructure diagram generated
- [ ] Multi-environment setup working (dev/staging/prod)

---

## 📚 Resources

- [LocalStack Documentation](https://docs.localstack.cloud/)
- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

---

**⬅️ [Previous: Kubernetes](../02-kubernetes-deployment) | [Next: CI/CD Pipeline →](../04-cicd-github-actions)**