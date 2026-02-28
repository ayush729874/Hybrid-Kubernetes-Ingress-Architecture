Now as i have implimented observilibility, now i will create a CI/CD pipeline for my app to update it automatically. I have decided to use Jenkins to achive this.

Git → Jenkins(test) → Worker1 builds & pushes image
                    → Jenkins(test) runs tests
                    → Jenkins(test) kubectl deploys to K8s
                                        ↓
                              Worker1 + Worker2 run pods
