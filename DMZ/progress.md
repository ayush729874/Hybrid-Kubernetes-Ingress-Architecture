☁️ Cloud VM Integration, Cluster Failure Analysis & Full Recovery

To expose the Kubernetes application publicly, I created a cloud VM on AWS and configured NGINX as a reverse proxy. The goal was to send all external traffic from the VM → Kubernetes Ingress Controller → Frontend/Backend.

🔌 Step 1: Connecting AWS VM to Kubernetes Node Using Tailscale

Installed Tailscale on both AWS instance and worker1
The worker1 node automatically switched its internal IP to the Tailscale-assigned IP
This caused Calico to break, as Calico was still expecting the original host IP

✔️ Fix Applied

Updated Calico DaemonSet to use the real host interface:

--auto-detect-interface=ens160


After this:

Calico nodes recovered
Worker1 regained internal IP 192.168.234.129
Cluster networking became healthy
In-cluster pod-to-pod connectivity worked fine

⚠️ Step 2: AWS VM Could Not Reach Kubernetes Ingress Controller

Even though the AWS instance could ping worker1 via Tailscale, it could not access:

Frontend
Backend
Ingress Controller
Browser access showed: 502 Bad Gateway

Tried multiple solutions on networking, routing, reverse proxy—but ingress traffic from AWS → cluster was consistently failing.

🧪 Step 3: Investigating Internal Application Failures

While checking pod connectivity inside the cluster:
Frontend → Backend = 500 Internal Server Error
Checked backend logs and found:
Access denied for user...

This indicated database authentication failure.

🧠 Root Cause: MySQL Data Loss Due to Pod Relocation

MySQL StatefulSet was scheduled on worker2
Worker2 node went down temporarily
MySQL pod moved to another node
The PVC was still attached to worker2, so the new pod started without data

Result:

Database deleted
Users deleted
Tables deleted

This caused backend to fail regardless of ingress or reverse proxy connectivity.

🔧 Fix: Node Affinity for MySQL StatefulSet

To prevent data loss:

Added nodeSelector to MySQL StatefulSet
→ Ensures MySQL only runs on worker2

Reattached the original PV and made it Available
Recreated DB, tables, and user credentials
Updated secrets in backend deployment
MySQL was now stable and persistent.

💥 Step 4: Full Cluster Networking Breakage

While validating cross-node connectivity, pods on one node could not reach pods on the other.
This confirmed Calico BGP & routing were broken at the cluster level.

After several days of troubleshooting attempts (IP auto-detect, MTU tuning, Calico reinstall, node resets), cluster networking remained unstable.

This indicated a deep-level cluster corruption.

🔁 Step 5: Final Solution — Rebuild Cluster Cleanly

Decided to create a fresh Kubernetes cluster from scratch, but this time with strict validation steps:

✔️ Improvements in the New Cluster

All nodes (master & workers) installed using the same Kubernetes version
Prevented API compatibility issues seen previously
Before deploying any application:
Created test pods on each node

Performed full cross-node connectivity tests
→ Pod ↔ Pod
→ Pod ↔ Service
→ DNS checks

Verified Calico routing was stable before proceeding

✔️ Deployment Order Followed

Install Ingress Controller first
Deploy MySQL StatefulSet
PV already existed on worker2, so MySQL came up with original data
Deploy Backend
Deploy Frontend
Apply Ingress resource

Validate end-to-end flow

🎉 Final Outcome

Cluster networking stable across all nodes
MySQL persistent and stable (no relocation issues)
Backend and frontend reachable through Ingress
AWS VM reverse proxy started working correctly
Application fully functional end-to-end

🏁 Key Takeaways & Learnings

Never allow Stateful apps (DB) to relocate unless storage matches
Always validate pod-to-pod cross-node communication before deployment
Tailscale may override node IPs → must explicitly set Calico auto-detect interface
Ingress troubleshooting must include NetworkPolicy, backend health, and DB connectivity
Version mismatch between master and worker nodes can break cluster stability
Sometimes rebuilding the cluster is faster than trying to revive a deeply broken environment


This time adding my worker2 in tailscale i insured that it won't affect my cluster IP.
After some confguration my frontend and backend was accessible from Cloud VM it self but when i tried to curl on localhost, it showd 502 error. After many troubleshhoting got to know that SELINUX is blocking the traffic. So after allowing the traffic my Website was accessed via Browser.
