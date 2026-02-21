# Self-Service Deployment Portal (IDP) - Assignment 2

## Overview
This project implements a simple Internal Developer Platform (IDP) backend that allows teams to:
- Register new microservices
- Trigger deployments (simulated CI/CD)
- View a health dashboard of services

It also includes a Terraform skeleton and reusable templates to demonstrate platform automation design.

---

## Backend API (FastAPI)

The backend runs on port 9000 and exposes the following APIs:

### 1. Register a Service
POST /register-service

Request body:
{
  "service_name": "user-metadata",
  "team_name": "platform",
  "repo_url": "https://github.com/example/user-metadata"
}

Response:
- Stores the service metadata in memory
- Returns the registered service

### 2. Trigger Deployment (Simulation)
POST /deploy/{service_name}

Response:
{
  "build_id": "<uuid>",
  "status": "QUEUED"
}

Behavior:
- Simulates a CI/CD pipeline in the background
- Status transitions: QUEUED -> RUNNING -> SUCCESS

### 3. Health Dashboard
GET /health

Response:
Returns a list of services with:
- service_name
- last_deployment_time
- deployment_status
- pod_count (mocked)
- cpu (mocked)
- memory (mocked)

---

## Terraform Structure

The terraform/ directory represents the platform automation layer:

- modules/ecr:
  - Creates an ECR repository for each service
- modules/iam:
  - Creates an IAM role for the service with least-privilege assumption policy
- modules/k8s-template:
  - Placeholder to represent Kubernetes manifest generation

This structure demonstrates how a real IDP would provision cloud resources per service.

---

## Templates

The templates/ directory contains reusable templates:

- deployment.yaml.tpl:
  - Kubernetes Deployment template for a service
- Jenkinsfile.tpl:
  - CI/CD pipeline template for build, push, and deploy stages

In a real system, these would be rendered with service-specific values and committed or applied automatically.

---

## Design Notes

- The CI/CD trigger is simulated to keep the assignment lightweight.
- The focus is on:
  - API design
  - Platform automation structure
  - Reusable templates
  - IDP / self-service workflow thinking
- The backend can be extended to:
  - Persist data in a database
  - Integrate real CI systems (Jenkins/GitLab)
  - Apply Terraform automatically

---

## How to Run

From 02-idp-deployment-portal/backend:

pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 9000

Then open:
http://localhost:9000/health
