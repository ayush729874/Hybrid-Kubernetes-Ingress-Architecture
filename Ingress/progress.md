🌐 Ingress Resource & Ingress Controller Integration

An Ingress resource was created to route external HTTP traffic as follows:

/ → Frontend Service
/submit → Backend Service

However, Ingress resources are only declarative objects.
They do nothing by themselves unless an Ingress Controller is actively watching and reconciling them.

🧠 Why an Ingress Controller Is Required

In Kubernetes, the control plane does not implement traffic routing logic for Ingress resources.

An Ingress Controller:
Watches Ingress objects
Translates rules into reverse-proxy configuration
Exposes services externally

Without a controller:
Ingress objects exist only in etcd
No routing, no IP, no traffic flow

🏗️ Ingress Controller Used

For this project, the Kubernetes community NGINX Ingress Controller maintained by Kubernetes was deployed.
It is based on open-source NGINX and is widely adopted in production clusters.

Installation Manifest (Bare Metal)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.1/deploy/static/provider/baremetal/deploy.yaml

📦 Resources Created by the Ingress Controller Manifest

Applying the controller manifest created all required components to securely manage Ingress traffic:

Namespace:
ingress-nginx

Service Accounts:
ingress-nginx
ingress-nginx-admission

RBAC:
Roles & RoleBindings
ClusterRoles & ClusterRoleBindings
→ Allow controller to watch Ingresses, Services, Endpoints, ConfigMaps, and Secrets

Controller Components:
Deployment: ingress-nginx-controller
ConfigMap: ingress-nginx-controller
Service: ingress-nginx-controller
Admission Webhook Services

Admission & Validation:
Admission Jobs (create / patch)
ValidatingWebhookConfiguration
IngressClass: nginx

These components together enable:
Secure operation
Dynamic config reloads
Validation of Ingress resources
Cluster-wide routing support

✅ Ingress Resource Activation Verification

Once the Ingress Controller became Running, the previously created Ingress resource was automatically reconciled.

kubectl get ingress
NAME              CLASS   HOSTS          ADDRESS           PORTS   AGE
treecom-ingress   nginx   treecom.site   192.168.234.129   80      12m

What This Confirms:
The Ingress Controller is actively watching Ingress resources
The controller assigned its Service IP to the Ingress
Routing rules are now live and functional
External traffic hitting 192.168.234.129 is processed by NGINX

End-to-End Traffic Flow:

Client
  ↓
Ingress Controller (NGINX)
  ↓
Ingress Rules
  ├── "/"        → Frontend Service
  └── "/submit"  → Backend Service

Key Takeaways:
Creating an Ingress resource alone is not sufficient
An Ingress Controller is mandatory to make routing effective
Address field in kubectl get ingress confirms controller attachment
RBAC, admission webhooks, and ingress class are critical for stability



