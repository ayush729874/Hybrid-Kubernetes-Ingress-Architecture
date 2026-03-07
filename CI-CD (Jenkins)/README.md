Now as i have implimented observilibility, now i will create a CI/CD pipeline for my app to update it automatically. I have decided to use Jenkins to achive this.

Till now create a pipeline which -> Checkes for changes in Repo and triggers the build. After that it detects changes on Frontend or Backend and creates Docker images from that code. Next it pushes the code to docker hub. After all of that it updates deployement yaml with latest build tag. That deployement is being watched by Argo CD and as soon as it detetcts any changes on that repo it deployes the same on test node.

After that i will create a test stage where testing will be performed and after succesful test code will be deployed on Production.

Developer pushes code to Git
        |
        ↓
Jenkins Pipeline (test node)
        |
        ├──→ Worker1 (Jenkins Agent)
        │      - Build Docker Image
        │      - Push to DockerHub
        |
        ├──→ Test Node
        │      - Selenium Tests
        │      - If tests fail → pipeline stops
        │      - If tests pass → proceed
        |
        └──→ ArgoCD
               - Watches Git repo
               - Deploys to K8s (Worker1/Worker2)
               - Rollback if deployment fails
