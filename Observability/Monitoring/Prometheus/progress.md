I am going to setup prometheus on my cluster using helm chart, so won't need to manage all the stuff manually. Chart will install
all the necessary things automatically.

Below is the prometheus chart which i will be using to setup promethous. I will be using default valuses as of now to deploy chart.
I will be changing values if required in future and update the chart.

This chart runs grafana pod by default so i will use the same as my Grafana setup pod.
"prometheus-community/kube-prometheus-stack"

To add helm chart first i added that repo in my helm after that simple installed chart.

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack
