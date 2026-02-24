# 🌐 Hybrid Kubernetes Ingress — Production-Grade Private Cluster

A self-hosted, production-grade Kubernetes deployment running on a **private bare-metal cluster**, securely exposed to the internet via a **DMZ architecture with Tailscale VPN** — no cloud load balancer, no managed Kubernetes.

---

## 🏗️ Architecture

```
Internet
    │
    ▼
┌─────────────────────────────┐
│   Ubuntu VPS  (DMZ Layer)   │  ← Only public-facing component
│   nginx reverse proxy       │
│   Public IP: exposed        │
└────────────┬────────────────┘
             │  Tailscale WireGuard Tunnel (encrypted)
             ▼
┌─────────────────────────────────────────────────────┐
│            Private Kubernetes Cluster               │
│                                                     │
│  socat → NodePort → NGINX Ingress Controller        │
│                          │                          │
│              ┌───────────┼───────────┐              │
│              ▼           ▼           ▼              │
│          Frontend     Backend      Observability    │
│                          │                          │
│                       MySQL                         │
│                    (StatefulSet)                    │
└─────────────────────────────────────────────────────┘
```

> The cluster nodes are **never exposed to the internet**. All public traffic enters through the VPS and is tunnelled securely into the cluster via Tailscale.

---

## 🧩 Stack

| Layer | Technology |
|---|---|
| Container Orchestration | Kubernetes (self-hosted) |
| CNI | Cilium (eBPF) |
| Ingress | NGINX Ingress Controller |
| VPN / Tunneling | Tailscale (WireGuard) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML/JS + NGINX |
| Database | MySQL (StatefulSet) |
| CI/CD | Jenkins |
| Metrics | Prometheus + Grafana |
| Logging | Loki + Grafana Alloy → AWS S3 |
| Security | NetworkPolicies, RBAC, Secrets, non-root containers |

---

## 📁 Repository Structure

```
├── Architecture_overview/     # Cluster setup and architecture docs
├── Backend/                   # FastAPI app, Dockerfile, K8s manifests
├── Frontend/                  # NGINX-served UI, Dockerfile, manifests
├── Database/                  # MySQL StatefulSet manifests
├── Ingress/                   # NGINX Ingress controller + resource manifests
├── CI-CD (Jenkins)/           # Jenkins deployment, PV/PVC, pipeline setup
├── Observability/
│   ├── Monitoring/            # Prometheus, Grafana dashboards, exporters
│   ├── Logging/               # Loki, Grafana Alloy, S3 configuration
│   └── Alerting/              # Alert rules and setup
├── Security/                  # NetworkPolicies, RBAC, security context docs
└── VPN/                       # Tailscale setup and socat bridge configuration
```

---

## 🔒 Security Highlights

- **Zero inbound ports** on cluster nodes — all traffic enters via Tailscale tunnel
- **NetworkPolicies** enforce strict pod-to-pod communication: `Ingress → Frontend → Backend → MySQL` only
- **Non-root containers** on both frontend and backend
- **readOnlyRootFilesystem** enforced via securityContext
- **Scoped RBAC** — each component runs with its own ServiceAccount and minimal permissions
- **Kubernetes Secrets** for all credentials — never hardcoded in manifests

---

## 📊 Observability

- **Prometheus** scrapes metrics from pods, nodes, MySQL exporter and ingress
- **Grafana** provides custom dashboards for cluster health, request rates and MySQL performance
- **Loki + Grafana Alloy** collects logs from all pods and ships them to **AWS S3** for long-term retention
- Alerting configured for pod crashes, high memory, and ingress errors

---

## 🔄 CI/CD Pipeline

Jenkins is deployed inside the cluster and automates the full delivery pipeline:

```
Git Push → Jenkins Webhook → Docker Build → Push Image → kubectl apply → Rolling Update
```

---

## 🌍 Why This Architecture?

Most tutorials use managed Kubernetes (EKS, GKE) with cloud load balancers. This project deliberately avoids that to demonstrate:

- How to securely expose a **private cluster** without a public IP on any node
- How to use **Tailscale** as a zero-config, zero-trust network bridge
- How to work around **Cilium eBPF NodePort** binding limitations
- How to build a **full observability stack** from scratch on self-hosted infrastructure
