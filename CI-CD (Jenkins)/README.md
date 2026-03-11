# 🚀 Treecom CI/CD Pipeline

A production-grade Jenkins pipeline for the [Treecom](https://treecom.site) URL shortening application. This pipeline automates the full software delivery lifecycle — from detecting code changes to deploying verified images to production — using Jenkins, Docker, ArgoCD, and Selenium.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Pipeline Stages](#pipeline-stages)
- [Prerequisites](#prerequisites)
- [Environment Variables & Credentials](#environment-variables--credentials)
- [Repository Structure](#repository-structure)
- [How It Works](#how-it-works)
- [Why This Pipeline?](#why-this-pipeline)
- [Deployment Flow Diagram](#deployment-flow-diagram)

---

## Overview

The Treecom pipeline follows a **GitOps-driven** approach:

- Application source code lives in [`jenkins-build`](https://github.com/ayush729874/jenkins-build)
- Kubernetes manifests live in a separate [`k8s_builds`](https://github.com/ayush729874/k8s_builds) repo
- ArgoCD watches the manifest repo and applies changes to the cluster automatically
- Jenkins orchestrates builds, tests, and manifest updates — it never deploys directly to Kubernetes

This separation of concerns prevents polling loops, keeps deployment history clean, and makes rollbacks trivial.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Developer                          │
│              git push → jenkins-build                   │
└────────────────────────┬────────────────────────────────┘
                         │ webhook / pollSCM
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Jenkins Pipeline                       │
│  Detect → Tag → Build → Push → Update Manifests         │
└────────────┬─────────────────────────┬──────────────────┘
             │                         │
             ▼                         ▼
      DockerHub Registry          k8s_builds repo
      ayush2744/frontend          test_builds/deployment.yaml
      ayush2744/backend           prod_builds/deployment.yaml
                                        │
                                        ▼
                               ┌────────────────┐
                               │    ArgoCD       │
                               │  Syncs cluster  │
                               └───────┬────────┘
                                       │
                        ┌──────────────┴──────────────┐
                        ▼                             ▼
               Test Environment               Production Environment
               test.treecom.site              treecom.site
```

---

## Pipeline Stages

### Stage 1 — Detect Changes
Compares the latest commit against its parent using `git diff --name-only HEAD~1 HEAD`. Only triggers a build if files inside `frontend/` or `backend/` were modified. This prevents unnecessary builds when only docs, configs, or unrelated files change.

Sets three environment flags:
| Flag | Purpose |
|---|---|
| `BUILD_FRONTEND` | `true` if frontend files changed |
| `BUILD_BACKEND` | `true` if backend files changed |
| `SHOULD_BUILD` | `true` if either service changed |

---

### Stage 2 — Checkout Source
Pulls the latest application source from the `jenkins-build` GitHub repository using SSH key authentication.

---

### Stage 3 — Resolve Image Tag
Queries the DockerHub API to find the latest published image tag (e.g. `v1.3`) and increments it automatically:

- `v1.9` → `v2.0` (minor version rolls over at 9)
- `v1.3` → `v1.4` (normal increment)
- No existing tags → starts at `v1.0`

This keeps versioning independent of Jenkins build numbers and makes DockerHub history meaningful.

---

### Stage 4 — Build
Runs `docker build` for whichever service(s) changed. Only the affected image is built — if only the backend changed, the frontend image is skipped entirely.

---

### Stage 5 — Publish to Registry
Logs into DockerHub using stored credentials and pushes the newly built image(s). Logs out immediately after.

---

### Stage 6 — Remove Local Images
Cleans up locally built images from the Jenkins agent after pushing, preventing disk bloat over time.

---

### Stage 7 — Update Test Manifest
Clones the `k8s_builds` manifest repository, updates the image tag in `test_builds/deployment.yaml` via `sed`, commits, and pushes back. ArgoCD detects this change and automatically syncs the test environment.

---

### Stage 8 — Deploy to Test
Triggers an ArgoCD sync for the `argocd-app` application (test environment) and waits up to **400 seconds** for the deployment to become fully healthy before proceeding.

---

### Stage 9 — Automated Tests
Runs `test.py` (Selenium-based end-to-end tests) against the live test environment at `test.treecom.site`. The stage retries up to **3 times** before failing. If tests fail, the pipeline halts and production is never touched.

---

### Stage 10 — Production Approval
Pauses the pipeline and presents a human approval prompt showing exactly which images are about to be deployed. The gate stays open for **24 hours** before timing out. A real human must click "Deploy to Production" to proceed.

---

### Stage 11 — Deploy to Production
After approval:
1. Clones `k8s_builds` and updates `prod_builds/deployment.yaml` with the new image tag
2. Commits and pushes the manifest change
3. Triggers ArgoCD sync for `argocd-prod` (production environment)
4. Waits up to **400 seconds** for the production deployment to become healthy
5. Confirms completion with a success message

---

## Prerequisites

| Tool | Purpose |
|---|---|
| Jenkins | Pipeline orchestration |
| Docker | Building and pushing images |
| ArgoCD CLI (`argocd`) | Triggering syncs and health checks |
| Python 3 + Selenium | Automated end-to-end tests |
| Git + SSH | Source checkout and manifest updates |

### Jenkins Agent
The pipeline runs on a node labelled `slave2-node-build`. Ensure this agent has Docker, ArgoCD CLI, Python 3, and Git installed.

---

## Environment Variables & Credentials

### Environment Variables (hardcoded)
| Variable | Value |
|---|---|
| `FRONTEND_IMAGE` | `ayush2744/frontend` |
| `BACKEND_IMAGE` | `ayush2744/backend` |
| `ARGOCD_SERVER` | `argocd.treecom.site:30437` |

### Jenkins Credentials Required
| Credential ID | Type | Used For |
|---|---|---|
| `jenkins` | SSH Username with private key | Cloning `jenkins-build` from GitHub |
| `dockerhub-credentials` | Username/Password | DockerHub login |
| `argocd-token` | Secret text | ArgoCD API authentication |

### SSH Config (on Jenkins agent)
The pipeline uses a host alias `github-manifests` for SSH operations against the `k8s_builds` repo. Ensure `~/.ssh/config` on the agent contains:

```
Host github-manifests
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_manifests
```

---

## Repository Structure

```
jenkins-build/               ← Application source (this repo)
├── frontend/
│   ├── Dockerfile
│   └── ...
├── backend/
│   ├── Dockerfile
│   └── ...
├── test.py                  ← Selenium test suite
└── Jenkinsfile              ← This pipeline

k8s_builds/                  ← Kubernetes manifests (separate repo)
├── test_builds/
│   └── deployment.yaml      ← Updated by Stage 7
└── prod_builds/
    └── deployment.yaml      ← Updated by Stage 11
```

---

## How It Works

1. A developer pushes code to `jenkins-build`
2. Jenkins detects the push and starts the pipeline
3. Only changed services are built and versioned
4. New Docker images are pushed to DockerHub
5. The test manifest is updated → ArgoCD deploys to test automatically
6. Selenium tests validate the live test environment
7. A human reviews and approves (or rejects) the production promotion
8. The prod manifest is updated → ArgoCD deploys to production automatically

---

## Why This Pipeline?

**Smart change detection** — Builds only what changed, saving time and compute on every run.

**Immutable versioning** — Every image gets a semantic version tag based on DockerHub history, making it trivial to identify, audit, or roll back any deployment.

**GitOps separation** — Application code and Kubernetes manifests are in separate repos. This means ArgoCD only watches manifests, Jenkins never talks directly to Kubernetes, and the cluster state is always fully described in Git.

**Automated quality gate** — Selenium tests run against a live test environment before production is ever considered. Three retries handle transient failures without false negatives.

**Human approval gate** — No code reaches production automatically. A 24-hour window gives teams time to review test results, coordinate release timing, or abort if something looks wrong.

**Self-cleaning agent** — Local Docker images are removed after each push, preventing the build agent from filling up its disk over time.

---

## Deployment Flow Diagram

```
git push
   │
   ▼
[Detect Changes] ──── No frontend/backend changes ──→ SKIP
   │
   ▼
[Checkout Source]
   │
   ▼
[Resolve Image Tag]  ← queries DockerHub API
   │
   ▼
[Build Images]       ← only changed services
   │
   ▼
[Push to DockerHub]
   │
   ▼
[Remove Local Images]
   │
   ▼
[Update Test Manifest] → git push → ArgoCD auto-syncs test env
   │
   ▼
[Wait for Test Deployment healthy]
   │
   ▼
[Run Selenium Tests] ── FAIL (3x) ──→ Pipeline aborted, prod safe
   │ PASS
   ▼
[Manual Approval Gate] ── Reject / Timeout ──→ Pipeline aborted
   │ Approve
   ▼
[Update Prod Manifest] → git push → ArgoCD auto-syncs prod env
   │
   ▼
[Wait for Production healthy]
   │
   ▼
✅ Live at treecom.site
```
