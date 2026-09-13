# CloudJob — Cloud-Native Data Processing Platform

CloudJob is a data-processing platform built to learn and demonstrate real-world DevOps practices: containerization, Kubernetes orchestration, CI/CD, Infrastructure as Code, GitOps, and observability.

## What it does

A user submits a data-processing job through an API. The job is scheduled onto Kubernetes as a workload, a worker processes the data, results are persisted, and the whole pipeline is monitored for success/failure.

```
Developer -> GitHub -> GitHub Actions -> Docker Image -> Container Registry -> Kubernetes -> API + Worker Jobs -> PostgreSQL / Object Storage
```

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

## Project status

Actively being built, in public, as a learning project. See commit history for progress.

## Build phases

1. FastAPI application
2. PostgreSQL integration
3. Dockerize
4. Docker Compose (local orchestration)
5. Kubernetes deployment
6. Kubernetes Jobs/CronJobs for processing
7. CI/CD with GitHub Actions
8. Push images to ECR
9. AWS infrastructure via Terraform
10. Helm packaging
11. GitOps with Argo CD
12. Prometheus + Grafana monitoring
13. Security, logging, observability hardening
