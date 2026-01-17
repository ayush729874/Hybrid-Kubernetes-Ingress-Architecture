Created an Image having logic and pushed it to Docker Hub.

Now created backend setup including below:

Config Map : Having DB details
Secret : Having DB login credentials as can not insert directoly while creating deployment.
Deployement : with 2 replicas , requests and limits , Environements
Service : created a clusterip service for backend.
Network Policy : Network policy which allows app=frontend traffic with ingree traffic
HPA : created a horizontal pod autoscalling to manage load.
