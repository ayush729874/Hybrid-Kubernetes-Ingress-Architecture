🧱 Backend Setup & Application Flow Validation

After building the custom backend image and pushing it to Docker Hub, the backend application was deployed on Kubernetes with all necessary components for a production-style setup.

🧩 Components Created
1. ConfigMap

Stores database hostname and port
Helps avoid hardcoding connection details inside deployment manifests

2. Secret

Stores database username and password securely
Injected as environment variables into the backend deployment

3. Deployment

2 replicas for availability
Resource requests & limits configured
Environment variables sourced from ConfigMap and Secret
Uses the custom backend image

4. Service (ClusterIP)

Exposes the backend internally
Allows frontend pods to reach backend via service name

5. NetworkPolicy

Restricts inbound traffic
Only allows ingress from pods with label:
**app=frontend**

6. Horizontal Pod Autoscaler (HPA)

Scales backend based on CPU utilization
Helps handle variable load automatically

🛠️ Debugging & Fixes

Issue 1: Incorrect Database Hostname

DB Service name: mysql-svc
ConfigMap used DB host as mysql → mismatch
Updated ConfigMap to use correct service name and restarted deployment
Backend connected successfully after fix

Issue 2: Wrong Database Port

MySQL StatefulSet exposed DB via a custom service port 8085
But ConfigMap was configured with 3306
Backend attempted to connect to a wrong port → Internal Server Error
Updated ConfigMap with correct port: 8085
After restart, DB connectivity was restored

🧪 Connectivity Testing

To verify the entire flow, a temporary frontend test pod was created:

kubectl run test-frontend \
  --image=curlimages/curl \
  --labels app=frontend \
  --restart=Never \
  -it -- sh

Test API Call

curl -X POST http://backend:8000/submit \
  -H "Content-Type: application/json" \
  -d '{"name":"ayush"}'

Result

API returned success
Data was inserted into the MySQL DB via backend

Database Output

mysql> select * from users;
+----+-------+
| id | name  |
+----+-------+
|  1 | ayush |
+----+-------+

✔️ Backend → MySQL flow validated successfully

Flow Explanation:

Frontend test pod sends POST request to backend
Backend processes request and connects to DB at mysql-svc:8085
DB receives the query and stores user data
Successful response returned from backend


                (Backend Pod)
             ┌────────────────────────┐
             │     backend app        │
             │                        │
             │  Connects to:          │
             │  mysql-svc:8085   ───────────────┐
             └────────────────────────┘          │
                                                 │ Service Port (8085)
                                                 ▼
                             ┌──────────────────────────────────┐
                             │   Kubernetes Service (mysql-svc) │
                             │  Type: ClusterIP                 │
                             │  Port:       8085                │
                             │  TargetPort: 3306                │
                             └──────────────────────────────────┘
                                                 │
                                                 │ Forwards traffic internally
                                                 ▼
                         ┌────────────────────────────────────────────┐
                         │         MySQL Pod (mysql-0)                │
                         │                                            │
                         │  MySQL Server listening on: 3306 (pod)     │
                         │                                            │
                         └────────────────────────────────────────────┘
