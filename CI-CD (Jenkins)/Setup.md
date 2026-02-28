Now as i have implimented observilibility, now i will create a CI/CD pipeline for my app to update it automatically. I have decided to use Jenkins to achive this.

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
