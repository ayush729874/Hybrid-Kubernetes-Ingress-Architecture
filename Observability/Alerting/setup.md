This repository documents a production-ready alerting setup built using Grafana Unified Alerting, leveraging both Prometheus (metrics) and Loki (logs) as data sources.

The goal of this setup is to ensure:

High availability of workloads
Early detection of infrastructure issues
Faster incident response
Reduced downtime
Proactive resource management

All alerts are designed following real-world production best practices to maintain cluster stability and application reliability.

🧠 Alerting Architecture

Metrics Source: Prometheus
Log Source: Loki
Alert Engine: Grafana Alerting
Notification Channel: Telegram

This allows unified monitoring of:

Infrastructure health
Kubernetes objects
Application behavior
Resource utilization
Crash and failure patterns

📌 Configured Production Alerts
🔹 Deployment Alerts
1️⃣ Deployment-ZeroReplicas
Triggers when a deployment has 0 running replicas, preventing complete application downtime before it impacts users.

2️⃣ Deployment-ReplicaMismatch
Detects mismatch between desired and available replicas, ensuring high availability and proper scaling behavior.

🔹 Node Alerts
3️⃣ Node-NotReady
Alerts when a node becomes NotReady, helping quickly isolate infrastructure or kubelet failures.

4️⃣ Node-HighCPU
Triggers when node CPU usage crosses threshold, preventing performance degradation due to resource exhaustion.

5️⃣ Node-HighMemory
Detects high memory consumption on nodes to avoid OOM events and workload eviction.

🔹 Pod Stability Alerts
6️⃣ Pod-CrashLoopBackOff
Identifies pods repeatedly crashing, enabling faster debugging of faulty deployments or runtime errors.

7️⃣ Pod-ImagePullBackOff
Detects image pull failures early, preventing broken releases from propagating in production.

8️⃣ Pod-OOMKilled
Triggers when containers are killed due to memory limits, helping optimize resource requests and limits.

9️⃣ Pod-StuckPending
Alerts when pods remain in Pending state, identifying scheduling, resource, or taint issues.

🔟 Pod-HighRestartRate
Detects abnormal restart patterns to proactively catch unstable applications before user impact.

🔹 Resource Utilization Alerts (Workload Level)
1️⃣1️⃣ Pod-HighCPU
Triggers when pod CPU usage exceeds threshold, helping identify scaling or optimization needs.

1️⃣2️⃣ Pod-HighMemory
Detects excessive memory usage at pod level to prevent application crashes and performance bottlenecks.

Covers infrastructure + workload + failure patterns
Prevents both hard failures and silent degradations
Uses both metrics (Prometheus) and logs (Loki) for deeper visibility
Designed for proactive monitoring instead of reactive firefighting
Supports multi-channel alert notifications
Scalable for large Kubernetes environments

🎯 Outcome

With this alerting framework in place:
MTTR (Mean Time To Recovery) is reduced
Downtime risk is minimized
Scaling issues are detected early
Application instability is caught before escalation
Cluster health remains continuously observable
