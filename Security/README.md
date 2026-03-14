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

2. Network Isolation (Added)
The cluster nodes are not directly internet-reachable. All external traffic enters through a cloud VM reverse proxy over a Tailscale VPN tunnel. Direct access to cluster NodePorts is blocked at the OS level via iptables rules on all nodes, covering the full Kubernetes NodePort range 30000-32767. This was validated by identifying and removing an unintentional socat-based relay service (tailscale-forward.service) that was previously exposing port 30437 publicly — discovered through ingress access log analysis showing direct public IPs hitting the cluster.


3. Rate Limiting (Added)
Rate limiting is implemented in two independent layers to prevent abuse of the URL shortening endpoint. Layer 1 on the cloud VM nginx uses limit_req_zone with raw TCP source IP — tamper-proof since no headers are involved — enforcing 10 req/min on /shorten and /api/* with a 100 req/min global flood limit. Layer 2 on the NGINX Ingress Controller acts as a backstop with proxy-real-ip-cidr locked to the VM's Tailscale IP, preventing header spoofing. Verified with live curl testing — correct 429 responses observed after burst exhaustion.
Known limitation: Per-IP rate limiting is ineffective against distributed botnet attacks where each bot uses a different IP. Cloudflare or a WAF in front of the reverse proxy would be the next step to address this.
