# SRE / Platform Engineering Assignments

This repository contains my solutions for four SRE / Platform Engineering assignments.  
Each assignment is kept in a separate folder for clarity.

---

## Repository Structure

- 01-user-metadata-service/ → Assignment 1 (Resilient Backend Service)
- 02-idp-deployment-portal/ → Assignment 2 (Platform / IDP Backend + Terraform + Templates)
- 03-k8s-observability-slo/ → Assignment 3 (Kubernetes + Observability + SLO)
- 04-security-compliance-design/ → Assignment 4 (Security & Compliance Design - Documentation)

---

## Assignment 1: User Metadata Service

Folder: 01-user-metadata-service/

- Python FastAPI backend service
- APIs:
  - POST /user
  - GET /user/{id}
- Reliability features:
  - Idempotency
  - Retry with exponential backoff and jitter
  - Circuit breaker for database layer
- Observability:
  - Prometheus metrics
  - Request logging with request_id and latency
- Containerized using Docker

---

## Assignment 2: IDP / Platform Engineering Backend

Folder: 02-idp-deployment-portal/

- FastAPI backend acting as a Self-Service Deployment Portal
- Features:
  - Register a new microservice
  - Trigger deployment (CI/CD simulation)
  - Health dashboard showing service status
- Includes:
  - Terraform skeleton (ECR, IAM, K8s template modules)
  - Reusable templates (Kubernetes Deployment, Jenkinsfile)
- Focus:
  - Platform engineering design
  - Self-service workflow
  - CI/CD and infrastructure automation structure

How to run:
- Go to 02-idp-deployment-portal/backend
- Install requirements
- Run: uvicorn backend.main:app --reload --host 0.0.0.0 --port 9000

---

## Assignment 3: Kubernetes + Observability + SLO

Folder: 03-k8s-observability-slo/

- Kubernetes manifests:
  - Deployment
  - Service
  - HPA (CPU + Memory)
  - PodDisruptionBudget
- Probes:
  - Liveness and Readiness using /health
- Observability:
  - Sample Grafana dashboard JSON
  - OpenTelemetry collector config
- SLO:
  - SLO document defining availability, latency, error budget, and alerts

---

## Assignment 4: Security & Compliance Design

Folder: 04-security-compliance-design/

- Documentation-only assignment
- Covers:
  - Secure CI/CD (SAST, DAST, secrets scanning)
  - IAM and least privilege
  - Service-to-service mTLS
  - PCI-DSS logging requirements
  - Audit log structure (PMLA style)
  - Secrets management and rotation
  - SBOM and supply chain security

---

## Notes

- Some parts (CI/CD, cloud resources, dashboards) are simulated or represented as templates and design documents, as per assignment instructions.
- The focus of this repository is on:
  - Reliability
  - Observability
  - Platform engineering
  - Security best practices

---

## Author

Vijay[D[D[D[D[DDunna SPC[D.[D[D.P.C.Vijay Kumar[D[D[D[D[D[D[D[D[C[C[C[C[C[C[C[C
