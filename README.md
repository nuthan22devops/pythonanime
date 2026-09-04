AnimeVerse — End-to-End DevOps CI/CD & Kubernetes Observability

Python Microservices • Docker • Jenkins • Kubernetes • Azure AKS • Argo CD • GitOps • Prometheus • Grafana • Alerting

AnimeVerse is a Python-based microservices application deployed on Azure Kubernetes Service (AKS) using an automated CI/CD and GitOps workflow.

The project demonstrates an end-to-end DevOps implementation covering:

Source control with GitHub
Continuous Integration using Jenkins
Docker containerization
Docker Hub image registry
Kubernetes orchestration
Azure Kubernetes Service (AKS)
Continuous Deployment using Argo CD
GitOps-based deployment
Automated application rollout
Kubernetes monitoring using Azure Managed Prometheus
Visualization using Azure Managed Grafana
Prometheus alerting rules
Email notifications when alert triggered

🏗️ Architecture
                         Developer
                             |
                             | git push
                             v
                        ┌──────────┐
                        │  GitHub  │
                        └────┬─────┘
                             |
                          Webhook
                             |
                             v
                     ┌──────────────┐
                     │    Jenkins   │
                     │     CI       │
                     └──────┬───────┘
                            |
              ┌─────────────┼─────────────┐
              |             |             |
           Build           Test        Docker Build
                                           |
                                           v
                                    ┌─────────────┐
                                    │  Docker Hub │
                                    └──────┬──────┘
                                           |
                                    Image update
                                           |
                                           v
                                    ┌─────────────┐
                                    │   GitHub    │
                                    │ K8s Manifests│
                                    └──────┬──────┘
                                           |
                                        GitOps
                                           |
                                           v
                                    ┌─────────────┐
                                    │   Argo CD   │
                                    └──────┬──────┘
                                           |
                                           v
                                  ┌────────────────┐
                                  │   Azure AKS    │
                                  │                │
                                  │ Microservices  │
                                  │ PostgreSQL     │
                                  └───────┬────────┘
                                          |
                                       Metrics
                                          |
                                          v
                              ┌────────────────────┐
                              │ Azure Managed      │
                              │ Prometheus         │
                              └─────────┬──────────┘
                                        |
                                      PromQL
                                        |
                                        v
                              ┌────────────────────┐
                              │ Azure Managed      │
                              │ Grafana             │
                              └─────────┬──────────┘
                                        |
                                      Alerts
                                        |
                                        v
                                  Email Notification.



Continuous Integration
Prerequisites

EC2 instance with sufficient memory to run Jenkins pipelines.

For the CI setup, I configured Jenkins, Docker, Git, and JDK on an EC2 instance.

After setting up Jenkins, I logged into the Jenkins UI. During the initial setup, Jenkins asks for the administrative password. The password can be retrieved by following the path provided by Jenkins and then entering it in the setup screen.
<img width="601" height="242" alt="image" src="https://github.com/user-attachments/assets/bf0ff4eb-11dd-40a6-bd9b-0c7d10493ede" />
After this, Jenkins provides the account setup where we configure the username and password for further usage.

After successfully setting up the credentials, I installed the suggested plugins as they are useful for most Jenkins use cases.
<img width="665" height="267" alt="image" src="https://github.com/user-attachments/assets/d1f75eb6-3b41-4b3a-9cc9-5d4dcb4a6395" />
From the Jenkins homepage, go to Manage Jenkins → Plugins.

I installed the Docker Pipeline plugin because Docker is used as an agent in the pipeline. This allows the pipeline to run inside a Docker-based environment, and the container is removed after the pipeline execution is completed.

Then, go to Manage Jenkins → Credentials and configure the required GitHub and Docker Hub credentials.

GitHub credentials can be used to checkout the repository if it is private. In my case, the repository is public. Docker Hub credentials are used to push the Docker images created during the pipeline execution.

The same credentials ID should be used in the Jenkins pipeline configuration to avoid authentication failures.
<img width="1247" height="297" alt="image" src="https://github.com/user-attachments/assets/a1b69426-8742-4cd2-9239-256c81e93d4e" />

From the Jenkins homepage, select New Item → Pipeline and provide a name for the pipeline.

I configured the pipeline to use the Jenkinsfile available in the Git repository by providing:

Repository URL
Branch to fetch
Jenkinsfile path
Required credentials, if the repository is private

After saving the configuration, the pipeline can be triggered using Build Now.

I configured four Jenkins pipelines for the four microservices in the application.
<img width="1340" height="550" alt="image" src="https://github.com/user-attachments/assets/7a828cfd-9bde-41c7-bb1d-6f6a548d5dc6" />

Jenkins Pipeline Stages

My Jenkins pipelines contain stages for:

Checkout source code
Install dependencies
Test the application
Build the application
Build the Docker image
Push the Docker image to Docker Hub
Update the Docker image in the Kubernetes manifest files

The updated Kubernetes manifests are then used as the desired state for GitOps-based Continuous Delivery.
<img width="1252" height="212" alt="image" src="https://github.com/user-attachments/assets/55fc17d3-6e33-47e2-b9f0-9081ed253e85" />
After the pipeline completes successfully, the newly built image is updated in the Kubernetes manifest files.

Continuous Deployment
Prerequisites

For Continuous Deployment, a Kubernetes cluster is required. In this project, I used Azure Kubernetes Service (AKS).

I configured Azure CLI and kubectl on my local machine/virtual machine and logged into the AKS cluster using Azure CLI.
<img width="547" height="222" alt="image" src="https://github.com/user-attachments/assets/11b01a8f-1750-418d-9c02-6a1cec0aaeb2" />

After connecting to the cluster, I created the argocd namespace and installed Argo CD.

To verify the Argo CD pods:

kubectl get pods -n argocd

To check the Argo CD services:

kubectl get svc -n argocd

I patched the Argo CD server service to LoadBalancer so that it could be accessed through a browser. The external address can be obtained using the service command
<img width="1161" height="422" alt="image" src="https://github.com/user-attachments/assets/fcf3f920-cfdf-43a5-8912-2be84d3cf221" />

Argo CD Login

To access Argo CD through the browser, I used the default administrator account.

Username: admin

The initial password can be retrieved using:

kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d

The retrieved password can then be used to log into the Argo CD homepage.
<img width="1335" height="687" alt="image" src="https://github.com/user-attachments/assets/6c52319c-fc0e-4744-8a1a-cbe2e0b839f0" />

In Argocd go to settings go to the repositories added via http and provided git repo url and click on connect Note:my account has been public there was no need of credentials
<img width="1347" height="347" alt="image" src="https://github.com/user-attachments/assets/b5ef6a03-86cf-421e-a8cf-1583cf354d86" />

Connect Git Repository

In Argo CD, go to Settings → Repositories and add the Git repository URL.

Since my repository is public, credentials were not required.
<img width="1315" height="512" alt="image" src="https://github.com/user-attachments/assets/3756e335-d0dd-4e6f-8632-dfadeff8b434" />
Create Argo CD Application

Go to Applications → New Application.

I configured:

Application name
Project
Sync policy
Git repository URL
Target namespace
Path containing Kubernetes manifests

I configured the sync policy as Automatic so that Argo CD can automatically synchronize changes from Git.
<img width="1342" height="631" alt="image" src="https://github.com/user-attachments/assets/45fb1670-9dce-43e8-ac11-c4e65c431323" />
Argo CD then deploys the application into the AKS cluster.
Verify Kubernetes Deployment

After the Argo CD deployment, I verified that the application pods and services were running in the Kubernetes cluster.
<img width="902" height="352" alt="image" src="https://github.com/user-attachments/assets/7880d036-3d1c-4bf7-a286-b0308da4d9cc" />
I changed the frontend-service to type LoadBalancer to expose the application externally.

The application can then be accessed through the external LoadBalancer address.

The deployed application was successfully accessed, and I was able to use the microservices and place an order.
<img width="1346" height="682" alt="image" src="https://github.com/user-attachments/assets/9ed37828-7a6d-4980-9615-c8ea516d0ed7" />
<img width="1337" height="662" alt="image" src="https://github.com/user-attachments/assets/601e07bc-4bd8-4ddf-9b07-e64778cacc32" />

Monitoring

I implemented monitoring for the Kubernetes cluster using Azure Managed Prometheus and Azure Managed Grafana to get visibility into resource utilization and cluster state.

After deploying the application, I configured Prometheus and Grafana for monitoring.

Azure Managed Grafana

In the Azure Portal, I created an Azure Managed Grafana resource.

To access Grafana, the required permissions need to be configured during setup.
After creating the Grafana resource, the Grafana URL can be found in the resource overview and used to access Grafana.
<img width="997" height="595" alt="image" src="https://github.com/user-attachments/assets/a76862c8-6fd1-434c-9c11-1a713a573437" />
Azure Monitor Workspace

Next, I created an Azure Monitor Workspace.

In the Access Control (IAM) section of the Monitor Workspace, I assigned the required monitoring permissions and provided access to the previously created Grafana resource.
<img width="982" height="600" alt="image" src="https://github.com/user-attachments/assets/693cdada-750e-4bf3-b4bf-7bd3ada3728c" />
<img width="1346" height="650" alt="image" src="https://github.com/user-attachments/assets/0b65eddb-92b9-41a7-9237-7c735213ee92" />


After creating the Grafana resource, the Grafana URL can be found in the resource overview and used to access Grafana.
<img width="1316" height="596" alt="image" src="https://github.com/user-attachments/assets/f91bc2f5-5e9b-4eb2-a1f1-d4d797ad2bcf" />
after the deployment succesfull now your azure monitor workspace will get the all metrics from the kubernetes cluster where grafana used to visualize the data coming to monitor workspace.
Now open grafana and go to data source you will be getting Azure monitor with Managed prometheus workspace.
<img width="1351" height="496" alt="image" src="https://github.com/user-attachments/assets/31450433-c752-487b-bf68-37515b18c39a" />
There were some default dashboard provided by Azure or set up your own.
<img width="1275" height="570" alt="image" src="https://github.com/user-attachments/assets/9ea1c082-4461-484f-a343-bb7f01ab5d63" />

Alerting:
We need to set up the alerting rule in order to get notified when the system breaks threesholds values.for that in azure portal go to monitoring--> alerts-->prometheus rule groups -->create a alerting rules through which you will get notified email or channel then --( microsoft will verify the gmail account before setting up alerts ,after succesfully verified the account then only it triggers males on alerts)-->add alert rule through PromQL expression provide annotation with summary and description of alert and save ( i have created a alert when a pod restart more than 3 times it will trigger the alert rule and i will be notified via provided email.)
<img width="1332" height="517" alt="image" src="https://github.com/user-attachments/assets/85372e59-d097-4c22-9ee3-d573bbb3c1b1" />

Now to test the alert we are delibaretly breaking a pod by deploying busybox image where the pod will throw error and restarts  then alert is triggering or not.
<img width="911" height="425" alt="image" src="https://github.com/user-attachments/assets/b88b8950-0e6a-4d93-b0f3-ef2d22f82440" />

As we checked we recieved alert notification via mail we configured.so the alerts are succesfully delivering when alert rules are triggered.
<img width="911" height="547" alt="image" src="https://github.com/user-attachments/assets/ede0564e-843c-432b-b120-f7478c44a25c" />
Therfore we can investigate the alert triggered reasons and act on issue earliest.


This Project helps me practical experience how to perform Continous integration through Jenkins pipeline and  Continous Deployment through Gitops via Argocd in kubernetes cluster. where in Continous Integration part i have been build pipeline for checkout SRC. building, testing application , and pushing the docker image to dockerhub and updating the latest image in the kubernetes manifest file

In Continous Deployment part we have set up Argocd in kubernetes cluster and added the repo of the updated kubernetes manifest to watch and sync automatically , and deployed those changes in cluster

I have also tested complete automation of the CICD by making the change in application interface for frontend and git commit main branch  which triggered the entire CICD proceess and we can see the newest version of image deployed in kubernetes cluster.








