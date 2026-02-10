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

There were some issue with environment variables which was not letting loki write on AWS S3 bucket so i tried many configuration and updated values yaml accordingly. After correctly defining the ENV's and enabled "-config.expand-env=true" which lets loki replace variable with actual secret values. Without this Loki assumes variable as String. This was the main issue my Loki server was not able to write logs on S3 Bucket.
After that there was time mismatch issue in logs so updated alloy to correct log timming. After all of that Loki was able to write logs on S3.

[Application Logs]
        ↓
[Grafana Alloy] → discovers, collects, parses, labels
        ↓ (HTTP Push API)
[Loki Distributor] → validates, rate limits, routes
        ↓ (internal gRPC)
[Loki Ingester] → buffers in memory, compresses into chunks
        ↓ (periodic flush)
[Amazon S3] → stores chunks + indexes permanently
        ↑ (query time)
[Loki Querier] → reads indexes, downloads chunks, filters
        ↓
[Query Results to User]


┌──────────────────────────────────────────────────────────┐
│                     Load Balancer                        │
└─────┬──────────────────────────────┬────────────────────┘
      │                              │
      │ (queries)                    │ (log ingestion)
      │                              │
┌─────▼──────────┐            ┌──────▼─────────┐
│  READ PATH     │            │  WRITE PATH    │
│                │            │                │
│ Query Frontend │            │  Distributor   │
│    Querier     │◄───────────┤   Ingester     │
└────────┬───────┘            └────────┬───────┘
         │                             │
         │                             │
         │         ┌───────────────────┘
         │         │
      ┌──▼─────────▼──┐
      │  BACKEND      │
      │               │
      │  Compactor    │
      │  Ruler        │
      │  Index Gateway│
      └───────┬───────┘
              │
         ┌────▼─────┐
         │ Storage  │
         │   (S3)   │
         └──────────┘

While setting UP loki as a data source, grafana shows unable to connect. So i tried to check all loki pods all of them were running fine but although issue was there. so i tried to check logs of pods and got to know Read pod was not able to Get connect with scheduler with It's IP. Then i checked and found shcduler is running within backend pod and backend pod was restarted as node was down for sometime and after restart backend pod IP got changed. So i resrated read pod and it found scheduler with it's current IP and run fine now. So in case of grafana, grafana runs few queries to stablish the connection and read pod is responsible for Queries that is why grafana was not able to connect. After that fix grafana was able to connect loki as a data source.
