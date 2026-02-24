This project focuses on deploying a production-style MySQL database on Kubernetes using manifests, with security, scalability, and observability in mind.

🧩 Components Deployed
MySQL deployed using StatefulSet
Service
Persistent Volumes & Persistent Volume Claims
SecurityContext (non-root execution)
NetworkPolicy for controlled access
Vertical Pod Autoscaler (VPA)
Metrics Server for resource metrics

📊 Vertical Pod Autoscaler (VPA) Setup

During VPA creation, the deployment initially failed because VPA Custom Resource Definitions (CRDs) were not installed. Since VPA is an optional Kubernetes add-on, it requires manual installation.

1. Install Metrics Server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

2. Install VPA CRDs and Components
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh


After installing the Metrics Server and VPA components, the VPA resource was created successfully.

🔐 SecurityContext Issue (Non-Root Execution)

After enabling runAsNonRoot, the MySQL pods failed to start due to the absence of a numeric user ID (UID).

✅ Fix Applied

Explicitly defined a numeric UID and filesystem group:

spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 999    # Standard MySQL UID
    fsGroup: 999      # Allows write access to mounted volumes


Once applied, the pods initialized correctly and persistent storage permissions were resolved.

🌐 Cluster Networking Issue & Recovery

While configuring the cluster, an internal IP was mistakenly set as the host IP.
This caused:

CoreDNS pods to fail
CNI pods to remain in a non-running state
Cluster networking to break completely

Despite multiple recovery attempts, the cluster remained unstable.

✅ Resolution

The cluster was re-created from scratch
Correct networking configuration was applied
Database manifests were re-deployed

After re-creation, all components (CNI, CoreDNS, MySQL, VPA) started successfully and worked as expected.

🎯 Key Learnings

VPA requires CRDs and Metrics Server and is not enabled by default
Kubernetes security contexts must include numeric UIDs when using non-root containers
Incorrect host IP configuration can break the entire cluster networking
In certain cases, cluster re-creation is faster and safer than deep recovery attempts

✅ Final Outcome

Fully functional Kubernetes cluster
Secure, non-root MySQL deployment
VPA working with controlled scaling
Stable networking and DNS resolution
Production-style database architecture

