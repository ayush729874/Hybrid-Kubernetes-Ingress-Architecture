🔐 Security
Overview
Security was implemented across multiple layers of the stack — from container runtime hardening to network-level isolation and secret management. The goal was to follow the principle of least privilege at every layer.

1. Container Security
Non-Root User
Both frontend and backend containers run as non-root users to prevent privilege escalation in case of container compromise.

Backend (Python/FastAPI)
Frontend (NGINX)

Read-Only Root Filesystem
Containers are prevented from writing to the root filesystem, limiting the blast radius of any runtime compromise.

Resource Limits & Requests
All pods have defined CPU and memory limits to prevent noisy neighbour issues and resource exhaustion attacks.

Network Policies

Traffic between pods is restricted using Kubernetes NetworkPolicies enforced by Cilium. The default posture is **deny-all**, with explicit allow rules only where needed.

Traffic Flow Allowed:

Internet → NGINX Ingress → Frontend → Backend → MySQL
                                ✗               ✗
                         (no direct)     (no direct from ingress/frontend)

Allow Ingress → Frontend only
Allow Frontend → Backend only
Allow Backend → MySQL only

Secrets Management
Sensitive values such as database credentials are stored as Kubernetes Secrets, never hardcoded in manifests or environment variables directly.

Secrets are injected into pods as environment variables:

Note: Kubernetes Secrets are base64 encoded by default. For production hardening, consider migrating to Sealed Secrets or an external secrets manager like AWS Secrets Manager or Vault.

RBAC & Service Accounts
Dedicated Service Accounts
Each component runs with its own ServiceAccount with only the permissions it needs, rather than using the default ServiceAccount.

Grafana Alloy RBAC
Grafana Alloy requires read access to pod logs and metadata across namespaces for log collection:
