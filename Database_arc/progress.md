Created all the component using manifest.

VPA creation was failed as it needs CDR's to be installed and which is a add on.
So installed a matric server and CDR manually using below step and after that VPA was created.

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# 1. Clone the autoscaler repository
git clone https://github.com/kubernetes/autoscaler.git

# 2. Navigate to the VPA directory
cd autoscaler/vertical-pod-autoscaler

# 3. Run the installation script
./hack/vpa-up.sh

After that pods were not getting up as i did not defined numeric user ID (UID) to use.
Pods were initiated after defining that.

spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 999  # Standard MySQL UID is often 999
    fsGroup: 999    # Ensures the container can write to mounted volumes

