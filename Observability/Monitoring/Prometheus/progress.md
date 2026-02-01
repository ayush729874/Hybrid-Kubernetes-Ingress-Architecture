🚀 Prometheus Setup on Kubernetes using Helm Chart
📋 Overview
This guide walks through setting up Prometheus on a Kubernetes cluster using the official Helm chart. The chart automatically installs all necessary components, including Grafana, making it easy to get a complete monitoring stack up and running.

🔧 Installation
Step 1: Add Helm Repository
First, add the Prometheus community Helm repository:
bashhelm repo add prometheus-community https://prometheus-community.github.io/helm-charts
Step 2: Install the Chart
Deploy Prometheus using the kube-prometheus-stack chart with default values:
bashhelm install prometheus oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack
```

> **💡 Note:** The chart includes Grafana by default, so you'll have a complete monitoring solution without additional setup.

---

## 🌐 Exposing Prometheus UI

### Understanding the Default Service

After deployment, Prometheus is exposed via a **ClusterIP** service, which means it's only accessible within the cluster. 

**Available options to expose externally:**
- **NodePort** - Opens a static port on each node
- **LoadBalancer** - Uses cloud provider's load balancer (for cloud environments)
- **Ingress** - ✅ Recommended for production

### Creating an Ingress Resource

Since an Ingress controller is already set up, I created a dedicated Ingress resource for Prometheus. This approach offers several benefits:

- ✅ More efficient for production environments
- ✅ Allows independent management of routing rules
- ✅ Doesn't impact existing Ingress configurations

**Configuration Details:**
- **Domain:** `prometheus.treecom.site`
- **Path:** `/`
- **Target Port:** `9090`

### Configure DNS Resolution

Add an entry to your hosts file:
```
192.168.234.130    prometheus.treecom.site treecom.site

⚙️ Monitoring Control Plane Components
🔴 The Challenge
The trickiest part of the setup is getting Prometheus to scrape control plane components. Here's why:
Problem: Prometheus attempts to scrape control plane components using the node IP, but control plane metrics are NOT exposed on the node IP. They're only available on:

127.0.0.1 (localhost)
Secured ports requiring client certificates

Result: Control plane components show as "down" in the Prometheus UI ❌

✅ The Solution
Instead of running a separate DaemonSet to collect metrics from each node (which would increase cluster resource usage and load), I used a more efficient approach:
1️⃣ Edit the Prometheus Server
Modified the prometheus-kube-prometheus-prometheus StatefulSet:
yamlspec:
  hostNetwork: true  # Added this to use host network
2️⃣ Schedule Prometheus on Control Plane Node
Added a node selector to ensure Prometheus runs on the control plane node itself:
yamlspec:
  nodeSelector:
    node-role.kubernetes.io/control-plane: ""

Why this works: By running Prometheus on the control plane with host networking enabled, it can collect metrics via localhost (127.0.0.1) directly.

3️⃣ Patch ServiceMonitors
Updated the ServiceMonitor configurations to point to the correct localhost addresses:
For kube-controller-manager:
yamlrelabelings:
  - sourceLabels: ["__address__"]
    targetLabel: "__address__"
    replacement: "127.0.0.1:10257"
For kube-scheduler:
yamlrelabelings:
  - sourceLabels: ["__address__"]
    targetLabel: "__address__"
    replacement: "127.0.0.1:10259"
For etcd:
yamlrelabelings:
  - sourceLabels: ["__address__"]
    targetLabel: "__address__"
    replacement: "127.0.0.1:2381"
4️⃣ Configure kube-proxy
Since kube-proxy runs on every node, edited the kube-proxy ConfigMap:
yamlmetricsBindAddress: "0.0.0.0:10249"  # Changed from 127.0.0.1:10249
This exposes kube-proxy metrics on all network interfaces instead of just localhost.

✅ Verification
After applying these configurations:

✅ All control plane components appear as "up" in the Prometheus UI
✅ Full visibility into cluster health and performance metrics
✅ Efficient resource utilization (no additional DaemonSet required)
