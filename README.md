**LogTester** 🧪🤖

AI-powered log analysis platform with a full DevOps toolchain

🚀 Overview

LogTester is a DevOps-oriented project that demonstrates how to build, test, package, and deploy an AI-assisted log analysis service using modern DevOps practices.

The application allows users to paste raw log output (Jenkins, Kubernetes, Docker, Python, or generic logs) and receive:

A clear explanation of the error

The most likely root cause

Actionable remediation steps

Confidence score

Extracted relevant log lines

🎯 The main goal of this project is to demonstrate DevOps skills, not frontend complexity or ML research.

🧠 Key Features

FastAPI backend with structured JSON responses

Human-friendly web GUI (HTML/CSS/JS)

AI-style log analysis engine (rule-based, extendable)

CI pipeline with Jenkins

Docker image build & push

Kubernetes deployment via Helm

Local Kubernetes using Minikube

Ready for GitOps / ArgoCD (next stage)

🏗 Architecture
```sh
User (Browser)
   |
   v
HTML / JS GUI  ──>  FastAPI (/analyze)
                          |
                          v
                  Log Analyzer Engine
                          |
                          v
                   Structured JSON Response

```
GitHub → Jenkins CI → DockerHub → Helm → Kubernetes (Minikube)

📂 Repository Structure
```sh

LogTester/
├── apps/
│   └── api/
│       ├── app/
│       │   ├── main.py          # FastAPI entrypoint
│       │   ├── analyzer.py      # Log analysis logic
│       │   ├── schemas.py       # Pydantic models
│       │   └── static/
│       │       └── index.html   # Web GUI
│       ├── tests/
│       │   └── test_health.py   # API tests
│       ├── Dockerfile
│       └── requirements.txt
│
├── helm/
│   └── logtester-api/
│       ├── templates/
│       │   ├── deployment.yaml
│       │   └── service.yaml
│       ├── values.yaml
│       └── Chart.yaml
│
├── Jenkinsfile
└── README.md
```
🧪 API Endpoints
| Method | Endpoint   | Description         |
| ------ | ---------- | ------------------- |
| GET    | `/`        | App metadata        |
| GET    | `/health`  | Health check        |
| POST   | `/analyze` | Analyze pasted logs |
| GET    | `/docs`    | Swagger UI          |

🖥 Web GUI
The web interface allows:

Pasting large log outputs

Selecting log source (Jenkins / Kubernetes / Docker / Python / Generic)

Viewing structured results with:

Explanation

Root cause

Step-by-step fixes

Confidence bar

Extracted error lines

Optional raw JSON toggle for advanced users

The GUI is served directly by FastAPI as static content.

🧩 CI – Jenkins Pipelineֿ
The Jenkins pipeline performs:

Checkout code from GitHub

Install dependencies

Run unit tests (pytest)

Build Docker image

Tag image with commit SHA + latest

Push image to DockerHub

Pipeline definition: Jenkinsfile

This ensures:

No image is built if tests fail

Every deployment is traceable to a Git commit

🐳 Docker
The API is packaged as a Docker image:
```sh
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY tests ./tests
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Images are pushed to DockerHub:
```sh
docker.io/<user>/logtester-api:<commit-sha>
docker.io/<user>/logtester-api:latest
```

☸ Kubernetes (Minikube)
Deployed to Kubernetes using Helm

Includes:

Deployment

Service

Liveness & readiness probes

Verified via:

kubectl logs

kubectl port-forward

/health endpoint

Example local access:
```sh
kubectl port-forward -n logtester svc/logtester-api 8000:8000
```
📦 Helm Deployment
Upgrade or install:
```sh

helm upgrade --install logtester-api ./helm/logtester-api \
  -n logtester \
  --set image.repository=docker.io/<user>/logtester-api \
  --set image.tag=latest
```
Rollout restart (when using latest):
```sh
kubectl rollout restart deployment -n logtester -l app=logtester-api

```
🔭 Observability (Current)

/health endpoint

Kubernetes liveness & readiness probes

Structured application logs (stdout)

🛣 Roadmap (Next Steps)

 Improve AI logic (LLM / prompt-based engine)

 Jenkins → Helm deployment automation

 GitOps with ArgoCD

 n8n integration (alerts, workflows)

 Metrics & monitoring

 More log source profiles

 Better error classification

 🎯 Why This Project Matters

This project demonstrates:

Real CI/CD workflows

Kubernetes & Helm in practice

Clean separation between API, UI, and deployment

Debugging real DevOps issues (images, paths, pipelines)

Production-style thinking, not just code

Perfect as:

GitHub portfolio project

Interview discussion anchor

Base for advanced GitOps work
