It dod not had any idea about loki. I only knew that it is used to collect logs. so i decided to study about loki before setting it up.
i got to know that there are three ways by which it can be deployed and i decided to go with Simple Scalable Mode. Before setting Loki
i wanted to decide where two store logs. there were two options one is locally store on a server or use cloud. So decide to go with
cloud. Firstly i was going to use Miniio but it sets several pods on cluster which could have caused extra load on cluster. so i decided
to start with S3 bucket. so created a S3 bucket and Policy and also generated Access Key and Secret Access key.

While searching over the internet that how loki works, i got to know there are several charts/ways to install loki. In which there was a chart called promtail and tried to know what is promtail and got to know it is a daemonset pod which collects logs from each node and push that logs to loki. but while searching for more information, i got to know that Promtail is going end of life on 2nd march 2026 and the modern replacement for Promtail is Grafana aloy which will be installed saparately and configured to push the logs to Loki.
