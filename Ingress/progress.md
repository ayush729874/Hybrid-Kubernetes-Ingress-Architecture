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

🧪 Ingress Connectivity Validation

After deploying the Ingress Controller and defining routing rules, the next step was to validate traffic flow from the Ingress to the application.

✔️ Step 1: Validate Frontend Traffic Through Ingress

Tested connectivity from worker1 using the NodePort exposed by the Ingress Controller:

curl -H "Host: treecom.site" http://192.168.234.129:31604/

Result:
Frontend page was returned successfully, confirming:

Ingress Controller is reachable
Ingress routing to frontend service is working
DNS-based host matching (Host: treecom.site) is functioning correctly
This validated the frontend path via the Ingress.

⚠️ Step 2: Backend API Call Failing With 504

Next, tested the /submit API that writes data into MySQL:

curl -H "Host: treecom.site" -X POST http://192.168.234.129:31604/submit -H "Content-Type: application/json" -d '{"name":"Ayush"}'


Result:
504 Gateway Timeout

A 504 means:

The Ingress Controller forwarded the request, but received no response from the backend within the timeout window.

So the issue was not Ingress → backend routing, but something blocking the backend path.

🕵️ Root Cause: NetworkPolicy Blocking Ingress → Backend Traffic

The backend NetworkPolicy was originally configured to allow traffic only from pods labeled app=frontend.

This meant:

Frontend → Backend ✔️ (allowed)
Ingress Controller → Backend ❌ (blocked)

Since the Ingress Controller resides in the ingress-nginx namespace, its traffic never matched the NetworkPolicy rules intended for frontend pods.

Therefore, backend returned no response, causing the 504 at Ingress.

🔧 Resolution: Allow Ingress Controller Namespace in NetworkPolicy

Updated the NetworkPolicy to allow ingress from:
Pods with label app=frontend
Pods from namespace ingress-nginx (Ingress Controller)

from:
- namespaceSelector:
    matchLabels:
      name: ingress-nginx


After applying the updated rules:
Ingress Controller was able to reach backend
/submit requests started working end-to-end

504 errors were resolved

✅ Final Outcome

The full request flow is now functional:
Client → Ingress Controller → Backend → MySQL

✔️ Frontend loads successfully
✔️ Backend API accepts POST requests
✔️ Data insertion into database is working
✔️ All namespaces now correctly permitted by NetworkPolicy

Pathced ingress controller to only get scheduled on worker1 as change in pod IP can cause network issues which can prevent DMZ to connect with Ingress Controller.

kubectl patch deployment ingress-nginx-controller -n ingress-nginx -p '{"spec": {"template": {"spec": {"nodeSelector": {"kubernetes.io/hostname": "worker1"}}}}}'
