# Hybrid-Kubernetes-Ingress-Architecture
This project showcases a real-world hybrid architecture where a public cloud VM acts as an external load balancer, forwarding internet traffic to a private Kubernetes cluster. An NGINX Ingress Controller handles internal routing to services and pods, commonly used when direct public exposure of Kubernetes nodes is restricted.

k8s-hybrid-ingress-architecture/
├── architecture/
│   ├── diagrams/
│   │   └── ingress-flow.png
│   └── design-decisions.md
├── ingress/
│   ├── ingress.yaml
│   └── notes.md
├── load-balancer/
│   ├── nginx.conf
│   └── README.md
├── security/
│   └── threat-model.md
├── troubleshooting/
│   └── real-issues-faced.md
└── README.md
