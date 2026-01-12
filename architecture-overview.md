User requests are received via a public cloud VM acting as a reverse proxy. Traffic is forwarded to a private Kubernetes cluster where an ingress controller performs routing. 
Requests are load-balanced through a service to application pods, which validate and process data before persisting it to a stateful SQL database.



User (Form Input)
   ↓
Domain (DNS)
   ↓
Cloud VM (Public IP)
[Reverse Proxy / Load Balancer]
   ↓
──────────── Kubernetes Cluster ────────────
Ingress Controller (NGINX)
   ↓
Service (ClusterIP)
   ↓
Application Pods (Deployment)
[Validation + Business Logic]
   ↓
Database Service (ClusterIP)
   ↓
Database Pod (StatefulSet + PV)
