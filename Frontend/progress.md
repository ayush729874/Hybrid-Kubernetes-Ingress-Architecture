🎨 Frontend Setup & Troubleshooting Summary

The frontend was designed as a lightweight, containerized web application served through Nginx and deployed on Kubernetes with autoscaling support.

🧩 Components Used

1. Docker Image

Created a simple web page
Placed the HTML files inside Nginx’s default /usr/share/nginx/html
Built and pushed a custom Docker image for deployment

2. ClusterIP Service

Exposes the frontend internally on port 80
Standard Nginx port; no additional configuration required

3. Deployment

Uses the custom Docker image
Includes resource requests and limits
Ensures predictable scheduling and better autoscaler behavior

4. Horizontal Pod Autoscaler (HPA)

Configured to automatically scale frontend replicas based on CPU usage

⚠️ Issue: Frontend Pods Not Starting

After deploying the manifests, frontend pods stayed in CrashLoopBackOff / Pending state.
Running a describe on the pods showed:

plugin type="calico" failed (add): error getting ClusterInformation: connection is unauthorized: Unauthorized

This clearly pointed to a CNI authorization issue.

🧠 Root Cause Analysis

The issue occurred because:
Calico ServiceAccount token may have expired or rotated
The Calico agent was unable to authenticate and fetch cluster networking data
As a result, CNI plugin could not attach networking to pods

When the CNI fails, all new pods remain stuck until networking is restored.

🔧 Resolution

Restarted the Calico DaemonSet:
kubectl rollout restart daemonset/calico-node -n calico-system

After the Calico nodes restarted:
CNI authorization recovered
Network interfaces started attaching properly
Frontend pods successfully came up

✅ Final Outcome

Frontend deployment became healthy
Pods received IP addresses properly

Service routing works as expected

HPA is now functional since metrics flow through the CNI
