Here i am desining Frontend.

Component used:

Docker Image: Created a web page and placed it on nginx default page and created a docker image to use that.
Cluster IP Service: Exposed frontend on port 80 as nginx listens on port 80 by default.
Deployment: Created deployement with my Own docker image and also used request and limits.
HPA: To autoscale the deployment.

Deployed the manifest but frontend pods were not getting up.
After describing pods i got to know error: "plugin type="calico" failed (add): error getting ClusterInformation: connection is unauthorized: Unauthorized"

There could be the reason:
Calico ServiceAccount token expired or got rotated

So i restarted calico daemon set. After calico pods were up frontend pods were up and running.
