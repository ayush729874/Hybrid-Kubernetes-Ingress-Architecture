User requests hit a public cloud VM, which forwards traffic to a Kubernetes ingress controller. 
The ingress routes requests to internal services, which load-balance traffic to application pods. 
The application persists data into a SQL database running as a stateful workload.



User (Browser)
   |
   |  HTTPS Request (Form Submit)
   v
Public Domain (DNS)
   |
   v
Cloud VM (Public IP)
[Reverse Proxy / Load Balancer]
   |
   |  Forward traffic (private IP / tunnel)
   v
---------------- Kubernetes Cluster ----------------

Ingress Controller (NGINX)
[Host + Path routing]
   |
   v
Service (ClusterIP)
[Internal load balancer]
   |
   v
Application Pods (Deployment)
[Form handling + validation + logic]
   |
   |  SQL queries
   v
Database Service (ClusterIP)
   |
   v
Database Pod (StatefulSet)
[Persistent Volume]

---------------------------------------------------

