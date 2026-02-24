🔒 VPN & Secure Tunneling — Tailscale
Overview
To securely bridge the public-facing Ubuntu VPS (DMZ layer) with the private Kubernetes cluster, Tailscale was implemented as a Zero-Trust VPN mesh network. This approach ensures that no Kubernetes node is ever directly exposed to the public internet, eliminating the need for open inbound firewall ports on the cluster side.

Problem Statement
The Kubernetes cluster runs on a private network with no public IP. The application needed to be accessible from the internet. The challenge was:

How to route public traffic to a private cluster securely
Without exposing NodePorts or cluster nodes to the internet
Without a cloud load balancer or managed Kubernetes service

Solution Architecture

Internet
    │
    ▼
Ubuntu VPS (Public IP: 160.250.204.213)
    │  nginx reverse proxy
    │
    ▼
Tailscale Tunnel (WireGuard encrypted)
    │  DERP Relay — Bangalore region
    │  VPS Tailscale IP: 100.94.184.84
    │  Worker2 Tailscale IP: 100.95.94.68
    │
    ▼
socat TCP Forward (worker2)
    │  Bridges Tailscale interface → internal NodePort
    │  socat TCP-LISTEN:30437 → TCP:192.168.234.130:30437
    │
    ▼
Cilium NodePort (192.168.234.130:30437)
    │  eBPF-based packet forwarding
    │
    ▼
NGINX Ingress Controller
    │  Host-based routing
    │
    ▼
Application Pods


How It Works

Enrollment — Both the Ubuntu VPS and the Kubernetes worker node (worker2) are enrolled in the same Tailscale network using the same account, forming a private mesh
Encrypted tunnel — All traffic between the VPS and cluster travels over WireGuard encryption, regardless of the underlying network path
DERP Relay — Since direct P2P connection could not be established between the VPS and worker node, Tailscale automatically falls back to its DERP relay infrastructure (Bangalore region), ensuring reliable connectivity without any manual configuration
socat bridge — Cilium CNI uses eBPF to handle NodePort traffic and does not bind NodePorts to the Tailscale interface. A socat forwarder runs as a systemd service on worker2 to bridge traffic arriving on the Tailscale IP to the internal NodePort
nginx proxy — On the VPS, nginx receives public HTTP traffic and proxies it to the worker node's Tailscale IP, with the correct Host header forwarded to the ingress controller