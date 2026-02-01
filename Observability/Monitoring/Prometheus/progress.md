I am going to setup prometheus on my cluster using helm chart, so won't need to manage all the stuff manually. Chart will install
all the necessary things automatically.

Below is the prometheus chart which i will be using to setup promethous. I will be using default valuses as of now to deploy chart.
I will be changing values if required in future and update the chart.

This chart runs grafana pod by default so i will use the same as my Grafana setup pod.
"prometheus-community/kube-prometheus-stack"

To add helm chart first i added that repo in my helm after that simple installed chart.

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack

After deploying all the component i checked prometheus server is being exposed with a cluster IP service which only allows it to
access within the cluster. There can a several way to expose it to Outside the cluster.
I can change that service type from cluster IP to Nodeport or in case of Cloud i could have used a load Balancer service to achive the same. But i have already setup a Ingress controller, so  i will route traffic to my Promethous server using ingress which is more effcieant way for production.

I created a saparate ingress resource for prometheus so can modify the rules saparately for my promethus server and it won't impact my existing rules.

This ingress resource will forward traffic from Domain **prometheus.treecom.site** with path "/" to port 9090 so i will be able to access the UI.

Before accessing the UI on browser, i need to add entry on Host file for the same.
192.168.234.130	prometheus.treecom.site treecom.site
