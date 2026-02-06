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
✅ APPLICATION HEALTH STATUS
Frontend Pods
Shows how many frontend pods are running — helps verify app availability.

Backend Pods
Shows how many backend pods are running — ensures API layer is healthy.

MySQL Pods
Shows active MySQL pod count — confirms database availability.

MySQL Connection
Shows if MySQL exporter can connect to DB — ensures DB is reachable for monitoring.

Success Rate (%)
Shows percentage of successful requests — helps detect API failures instantly.

✅ TRAFFIC & PERFORMANCE
Request Rate – Traffic Flow
Shows how many requests hit the application per second — helps understand load patterns.

Response Time – Percentiles (p50/p95/p99)
Shows median and slowest request times — helps identify performance issues.

✅ SUMMARY STATISTICS
Frontend Pod Count
Counts running frontend pods — confirms frontend scaling.

Backend Pod Count
Counts running backend pods — ensures backend scaling.

Database Pod Count
Counts running MySQL pods — confirms DB redundancy (if used).

Total App Pods
Shows all app-related pods — gives a quick full system health snapshot.

Total Requests (24h)
Shows total site hits in 24 hours — helps track traffic volume.

Total Memory Used
Shows total RAM used across all app pods — helps measure resource consumption.

✅ GAUGES
Success Rate Gauge
Shows real-time successful request percentage — instantly highlights failures.

Error Rate Gauge
Shows number of failed requests per second — helps detect issues early.

DB Connections Gauge
Shows current MySQL connection usage — helps prevent connection overload.

✅ FRONTEND TIER
Frontend CPU Usage
Shows per-pod CPU usage — helps detect overloaded frontend pods.

Frontend Memory Usage
Shows per-pod RAM usage — identifies memory leaks or spikes.

✅ BACKEND TIER
Backend CPU Usage
Shows backend pod CPU usage — helpful for scaling decisions.

Backend Memory Usage
Shows backend RAM usage — detects heavy memory consumers.

✅ DATABASE TIER – MYSQL
MySQL Connections
Shows active, max-used, and max-allowed connections — helps avoid too many connections.

MySQL Query Rate by Type
Shows SELECT/INSERT/UPDATE/DELETE rates — helps understand query load patterns.

MySQL CPU Usage
Shows MySQL CPU use per pod — useful for detecting heavy workloads.

MySQL Memory Usage
Shows RAM used by MySQL — helps ensure DB cache is sized correctly.

InnoDB Buffer Pool Reads
Shows how often MySQL had to read from disk — helps detect slow disk access.

Slow Queries
Shows queries that exceeded slow-query threshold — helps find performance bottlenecks.

Buffer Pool Hit Ratio
Shows % of queries served from RAM — indicates database performance efficiency.

✅ APPLICATION PODS SECTION
Pod Status Table
Shows running status of each pod — quickly highlights failing pods.

Pod Restart Counts
Shows how many times each container restarted — helps detect crashes or instability.

🧩 Result

This custom monitoring setup now provides:
Full observability for Treecom’s core services
Quick detection of performance degradation
Deep database insights for optimizing queries
A centralized view for SRE/DevOps operations

After observing the dashboard for few days, i thought i should monitor rows count as well so i added that graph on top. After that i updated few records on the table but records were not updated. then after some research i got to know, i will have to analyze the table which reads all the indexes on the table and update the count. So i schedule a cron job which will analyze DB on each 30 min which will Update Rows count on the dashboard.
