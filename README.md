# Data Pipeline DevOps Project

This is a data-processing platform built to learn and show DevOps practices: containerization, Kubernetes orchestration, CI/CD, Infrastructure as Code, GitOps, and observability.

## What it does

A user submits a data-processing job through an API. The job is scheduled onto Kubernetes as a workload, a worker processes the data, results are persisted, and the whole pipeline is monitored for success/failure.


## Tech stack

| Layer | Tool |
|---|---|
| Backend API | Python + FastAPI |
| Database | PostgreSQL |
| Containers | Docker |
| Local orchestration | Docker Compose |
| Orchestration | Kubernetes |
| Cloud provider | AWS |
| Infrastructure as Code | Terraform |
| Container registry | Amazon ECR |
| CI/CD | GitHub Actions |
| Packaging | Helm |
| GitOps | Argo CD |
| Monitoring | Prometheus + Grafana |
| Reverse proxy / LB | Nginx / AWS Load Balancer |
| Security | IAM, Kubernetes Secrets, least privilege |