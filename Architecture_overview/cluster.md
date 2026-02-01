[root@controlplane ~]# kubectl get all -A
NAMESPACE       NAME                                            READY   STATUS    RESTARTS        AGE
default         pod/backend-745c8ffcd7-p9dql                    1/1     Running   0               6d15h
default         pod/backend-745c8ffcd7-scf62                    1/1     Running   0               6d15h
default         pod/frontend-66f856b957-9vlxf                   1/1     Running   0               6d14h
default         pod/frontend-66f856b957-k6sl7                   1/1     Running   0               6d14h
default         pod/mysql-0                                     1/1     Running   0               6d18h
ingress-nginx   pod/ingress-nginx-controller-66b9895f54-5g4ts   1/1     Running   0               6d16h
kube-system     pod/cilium-5gxrk                                1/1     Running   0               6d18h
kube-system     pod/cilium-b6tbt                                1/1     Running   0               6d18h
kube-system     pod/cilium-envoy-ddz2m                          1/1     Running   0               6d18h
kube-system     pod/cilium-envoy-wthf8                          1/1     Running   0               6d18h
kube-system     pod/cilium-envoy-x4pjv                          1/1     Running   0               6d18h
kube-system     pod/cilium-jxgq9                                1/1     Running   0               6d18h
kube-system     pod/cilium-operator-584695ccd8-8bhgv            1/1     Running   4 (8m24s ago)   6d18h
kube-system     pod/coredns-76f75df574-8j74l                    1/1     Running   0               6d18h
kube-system     pod/coredns-76f75df574-ltnwn                    1/1     Running   0               6d18h
kube-system     pod/etcd-controlplane                           1/1     Running   0               6d18h
kube-system     pod/kube-apiserver-controlplane                 1/1     Running   0               6d18h
kube-system     pod/kube-controller-manager-controlplane        1/1     Running   3 (8m52s ago)   6d18h
kube-system     pod/kube-proxy-6hhss                            1/1     Running   0               6d18h
kube-system     pod/kube-proxy-cqzjx                            1/1     Running   0               6d18h
kube-system     pod/kube-proxy-gv97q                            1/1     Running   0               6d18h
kube-system     pod/kube-scheduler-controlplane                 1/1     Running   4 (8m46s ago)   6d18h
kube-system     pod/metrics-server-59d465df9f-f2vsg             1/1     Running   0               6d18h
kube-system     pod/vpa-admission-controller-cd698f44d-smj6q    1/1     Running   0               6d18h
kube-system     pod/vpa-recommender-796d45bfdf-8bppf            1/1     Running   0               6d18h
kube-system     pod/vpa-updater-7548dbc57d-zj2rt                1/1     Running   0               6d18h

NAMESPACE       NAME                                         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
default         service/backend                              ClusterIP   10.103.150.145   <none>        8000/TCP                     6d17h
default         service/frontend                             ClusterIP   10.109.214.215   <none>        80/TCP                       6d17h
default         service/kubernetes                           ClusterIP   10.96.0.1        <none>        443/TCP                      6d18h
default         service/mysql-svc                            ClusterIP   10.102.48.96     <none>        3306/TCP                     6d18h
ingress-nginx   service/ingress-nginx-controller             NodePort    10.106.115.108   <none>        80:30437/TCP,443:32228/TCP   6d18h
ingress-nginx   service/ingress-nginx-controller-admission   ClusterIP   10.103.181.140   <none>        443/TCP                      6d18h
kube-system     service/cilium-envoy                         ClusterIP   None             <none>        9964/TCP                     6d18h
kube-system     service/hubble-peer                          ClusterIP   10.101.162.233   <none>        443/TCP                      6d18h
kube-system     service/kube-dns                             ClusterIP   10.96.0.10       <none>        53/UDP,53/TCP,9153/TCP       6d18h
kube-system     service/metrics-server                       ClusterIP   10.99.160.29     <none>        443/TCP                      6d18h
kube-system     service/vpa-webhook                          ClusterIP   10.100.163.197   <none>        443/TCP                      6d18h

NAMESPACE     NAME                          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   daemonset.apps/cilium         3         3         3       3            3           kubernetes.io/os=linux   6d18h
kube-system   daemonset.apps/cilium-envoy   3         3         3       3            3           kubernetes.io/os=linux   6d18h
kube-system   daemonset.apps/kube-proxy     3         3         3       3            3           kubernetes.io/os=linux   6d18h

NAMESPACE       NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
default         deployment.apps/backend                    2/2     2            2           6d17h
default         deployment.apps/frontend                   2/2     2            2           6d17h
ingress-nginx   deployment.apps/ingress-nginx-controller   1/1     1            1           6d18h
kube-system     deployment.apps/cilium-operator            1/1     1            1           6d18h
kube-system     deployment.apps/coredns                    2/2     2            2           6d18h
kube-system     deployment.apps/metrics-server             1/1     1            1           6d18h
kube-system     deployment.apps/vpa-admission-controller   1/1     1            1           6d18h
kube-system     deployment.apps/vpa-recommender            1/1     1            1           6d18h
kube-system     deployment.apps/vpa-updater                1/1     1            1           6d18h

NAMESPACE       NAME                                                  DESIRED   CURRENT   READY   AGE
default         replicaset.apps/backend-5d4466bf97                    0         0         0       6d17h
default         replicaset.apps/backend-67c84f47f                     0         0         0       6d15h
default         replicaset.apps/backend-745c8ffcd7                    2         2         2       6d15h
default         replicaset.apps/frontend-5dc99c8898                   0         0         0       6d14h
default         replicaset.apps/frontend-65446c8847                   0         0         0       6d17h
default         replicaset.apps/frontend-66f856b957                   2         2         2       6d14h
default         replicaset.apps/frontend-86679686d6                   0         0         0       6d14h
ingress-nginx   replicaset.apps/ingress-nginx-controller-66b9895f54   1         1         1       6d16h
ingress-nginx   replicaset.apps/ingress-nginx-controller-74886f686b   0         0         0       6d18h
kube-system     replicaset.apps/cilium-operator-584695ccd8            1         1         1       6d18h
kube-system     replicaset.apps/coredns-76f75df574                    2         2         2       6d18h
kube-system     replicaset.apps/metrics-server-59d465df9f             1         1         1       6d18h
kube-system     replicaset.apps/metrics-server-856f767b               0         0         0       6d18h
kube-system     replicaset.apps/vpa-admission-controller-cd698f44d    1         1         1       6d18h
kube-system     replicaset.apps/vpa-recommender-796d45bfdf            1         1         1       6d18h
kube-system     replicaset.apps/vpa-updater-7548dbc57d                1         1         1       6d18h

NAMESPACE   NAME                     READY   AGE
default     statefulset.apps/mysql   1/1     6d18h

NAMESPACE   NAME                                               REFERENCE             TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
default     horizontalpodautoscaler.autoscaling/backend-hpa    Deployment/backend    3%/70%    2         5         2          6d17h
default     horizontalpodautoscaler.autoscaling/frontend-hpa   Deployment/frontend   0%/70%    2         5         2          6d17h
[root@controlplane ~]#
