Created an Image having logic and pushed it to Docker Hub.

Now created backend setup including below:

Config Map : Having DB details
Secret : Having DB login credentials as can not insert directoly while creating deployment.
Deployement : with 2 replicas , requests and limits , Environements
Service : created a clusterip service for backend.
Network Policy : Network policy which allows app=frontend traffic with ingree traffic
HPA : created a horizontal pod autoscalling to manage load.

tried to test the flow with a frontend labled test pod. There is internal server error.

Service for DB was created with name mysql-svc and i had defined host name "mysql" in configmap. so udated deployement and restarted the same.

I had created a custon service port 8085 but in config map i selected db port to 3306. as my db is using 8085 port to except traffic so there was issue with connectivity.
Updated the same and now able to insert in to table from backend pods.

                (Backend Pod)
             ┌────────────────────────┐
             │     backend app        │
             │                        │
             │  Connects to:          │
             │  mysql-svc:8085   ───────────────┐
             └────────────────────────┘          │
                                                 │ Service Port (8085)
                                                 ▼
                             ┌──────────────────────────────────┐
                             │   Kubernetes Service (mysql-svc) │
                             │  Type: ClusterIP                 │
                             │  Port:       8085                │
                             │  TargetPort: 3306                │
                             └──────────────────────────────────┘
                                                 │
                                                 │ Forwards traffic internally
                                                 ▼
                         ┌────────────────────────────────────────────┐
                         │         MySQL Pod (mysql-0)                │
                         │                                            │
                         │  MySQL Server listening on: 3306 (pod)     │
                         │                                            │
                         └────────────────────────────────────────────┘
