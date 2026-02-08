It dod not had any idea about loki. I only knew that it is used to collect logs. so i decided to study about loki before setting it up.
i got to know that there are three ways by which it can be deployed and i decided to go with Simple Scalable Mode. Before setting Loki
i wanted to decide where two store logs. there were two options one is locally store on a server or use cloud. So decide to go with
cloud. Firstly i was going to use Miniio but it sets several pods on cluster which could have caused extra load on cluster. so i decided
to start with S3 bucket. so created a S3 bucket and Policy and also generated Access Key and Secret Access key.

While searching over the internet that how loki works, i got to know there are several charts/ways to install loki. In which there was a chart called promtail and tried to know what is promtail and got to know it is a daemonset pod which collects logs from each node and push that logs to loki. but while searching for more information, i got to know that Promtail is going end of life on 2nd march 2026 and the modern replacement for Promtail is Grafana aloy which will be installed saparately and configured to push the logs to Loki.

Why Alloy is Better:

More versatile - Can collect logs, metrics, traces, and profiles (not just logs)
Better performance - More efficient resource usage
Active development - Getting new features and improvements
Unified agent - One agent for all observability data
Better pipeline configuration - More flexible log processing

First of all i extracted values of chart grafana/loki. Now created a secret containing details of my AWS S3 bucket accesskey and secret access key and injected those on values as environment variable. After that configured S3 bucket on that and deployed that chart but all the pods were waiting for PVC so i uninstalled chart and read whole value yaml and disable each PVC (read,write,backend and binary) so they by defualt use S3 for storing logs and also configured chunks-cache according my cluster confuguration. After all the configuration My loki server was up and running.
