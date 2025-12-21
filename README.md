LogTester 🧪🤖

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
sh```
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
