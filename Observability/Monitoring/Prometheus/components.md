Core Components:
prometheus-kube-prometheus-prometheus - Main Prometheus server that scrapes and stores time-series metrics data
prometheus-kube-prometheus-alertmanager - Handles alerts sent by Prometheus, manages deduplication, grouping, and routing to notification channels
prometheus-grafana - Web-based visualization and analytics platform for viewing Prometheus metrics through dashboards
prometheus-kube-prometheus-operator - Kubernetes operator that manages Prometheus, Alertmanager, and related monitoring components lifecycle

Exporters & Metrics Collection:
prometheus-prometheus-node-exporter - DaemonSet that exposes hardware and OS-level metrics from each Kubernetes node
prometheus-kube-state-metrics - Generates metrics about Kubernetes objects (pods, deployments, nodes, etc.) state

ServiceMonitors:
ServiceMonitor resources - Custom resources that tell Prometheus which services to scrape for metrics (apiserver, kubelet, coredns, etcd, etc.)

Configuration & Rules:
PrometheusRule resources - Define alerting and recording rules for metrics evaluation and alert triggering
ConfigMaps (dashboards) - Pre-configured Grafana dashboards for visualizing cluster, workload, and resource metrics
prometheus-kube-prometheus-grafana-datasource - ConfigMap that configures Prometheus as a data source in Grafana

Access Control:
ServiceAccounts - Kubernetes identities for running Prometheus components with appropriate permissions
ClusterRoles/ClusterRoleBindings - Grant cluster-wide read permissions to scrape metrics from Kubernetes API and resources
Roles/RoleBindings - Namespace-specific permissions for component operations

Services:
ClusterIP Services - Internal endpoints for accessing Prometheus (9090), Grafana (80), Alertmanager (9093), and exporters
Headless Services (ClusterIP: None) - Direct pod-to-pod communication for scraping Kubernetes core components (etcd, scheduler, controller-manager, etc.)
Admission Control:
MutatingWebhookConfiguration - Automatically injects sidecar containers for secret reloading
ValidatingWebhookConfiguration - Validates Prometheus/Alertmanager custom resource configurations before creation

Secrets:
prometheus-grafana - Stores Grafana admin credentials
alertmanager-prometheus-kube-prometheus-alertmanager - Stores Alertmanager configuration
