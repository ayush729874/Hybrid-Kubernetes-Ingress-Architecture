🚀 Overview

The goal of this monitoring setup is to create a dedicated, production-ready observability system for the Treecom Application.
Since existing dashboards were either generic or insufficient for deep application insights, a custom Grafana dashboard was built to track application performance, database health, and infrastructure-level signals.

This documentation explains why the setup was required, how it was implemented, and what the dashboard monitors.

🎯 Why This Monitoring Setup Was Needed

Treecom consists of multiple components—Frontend, Backend, and MySQL DB.
To ensure reliable performance and quick issue detection, I needed:

Application-specific metrics
Database-level health indicators
End-to-end visibility of requests, errors, and resource usage

The default dashboards did not provide this depth, so a custom solution was necessary.

🛠️ Architecture Summary
1. MySQL Metrics Exposure via MySQL Exporter

Before creating the dashboard, DB metrics had to be exposed.
To achieve this:

Deployed a MySQL Exporter Pod inside the cluster
Created a Kubernetes Secret containing DB credentials (non-root user)
Configured MySQL Exporter to authenticate using this secret

Network Policy Adjustment

Initially, MySQL Exporter could not reach the MySQL Pod because of a restrictive network policy allowing only the backend to access DB.

To fix this:

Updated the NetworkPolicy to allow the MySQL Exporter Pod to access the MySQL Pod.
This enabled Prometheus to scrape DB health metrics successfully.

📈 Custom Production-Grade Dashboard

Once metrics from all components were available, a complete production-level Grafana dashboard was created.
It includes critical graphs and KPIs required for real-time monitoring and troubleshooting.

🔍 Dashboard Metrics & Visualizations
1. Running Pod Count

Frontend
Backend
MySQL

2. Success Rate

Overall application success percentage
Error rate trends

3. Request Rate & Response Time

Requests/second
Latency patterns

4. 24-Hour Total Requests & Memory Usage

Daily traffic summary
Total memory consumed by the system

5. Success Rate Errors & DB Connection Metrics

Errors vs. successful requests
DB connection health status

6. Frontend Resource Utilization

CPU usage
Memory usage

7. Backend Resource Utilization

CPU usage
Memory usage

8. MySQL Metrics

Active MySQL connections
Query rate by query type
Slow query monitoring
CPU & memory usage

9. InnoDB Engine Health

Buffer pool reads
Buffer pool hit ratio
Slow queries analysis

10. Pod Health Metrics

Pod status
Restart counts

Stability analysis over time

🧩 Result

This custom monitoring setup now provides:
Full observability for Treecom’s core services
Quick detection of performance degradation
Deep database insights for optimizing queries
A centralized view for SRE/DevOps operations
