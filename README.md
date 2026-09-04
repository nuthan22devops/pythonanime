End to End CICD Project using Jenkins as Continous Integration & GitOPS Argocd for Continous Deployment 
# AnimeVerse — Python Microservices Demo

A simple anime shopping application built with 4 Python microservices + PostgreSQL
1.frontend 2.catalog 3.checkout 4.order-service 5.postgreSQL
All these 5 microservices has been build with chatgpt
Jenkinsfiles,Dockerfiles, and kubernetes manifest files has been devoloped using offical documentation for each microservice.

Continous integration:
Prerequisites: EC2 instance with good memory to run the jenkins pipelines.we configured and set up the jenkins application,docker,git, jdk  for CI part in  EC2 instance.
After setting up the jenkins we have logged &into jenkins ui, then it asks for the login adminstrative password you can follow the path it provides and retrive the passwordand paste it there and enter. <img width="601" height="242" alt="image" src="https://github.com/user-attachments/assets/bf0ff4eb-11dd-40a6-bd9b-0c7d10493ede" />
 you will be now get the account setup where you need to configure your Username &Password to access jenkins for further usage.
after succesfully setting up credentials ,Always start jenkins with installed suggested plugins as they are useful in most cases.
<img width="665" height="267" alt="image" src="https://github.com/user-attachments/assets/d1f75eb6-3b41-4b3a-9cc9-5d4dcb4a6395" />
In Homepage go to settings-->plugins-->install-->plugins** We have installed Docker pipeline plugin as we are using docker as a agent in pipeline, so that it will run the pipeline in a container type environment, and  after executing the pipeline regardless of success or failure of job, it will destroy the docker container.

Then, go to Security-->credentials and configure your github and dockerhub credentials as the github credentials are used to checkout the repo incase if its private in our case our repo is public dockerhub credentials are used to push your dockerimage to dockerhub which will be built while executing the pipeline. Note please use the credentials id as same when declaring them in jenkins pipeline too in order to prevent failure while authenticating.
<img width="1247" height="297" alt="image" src="https://github.com/user-attachments/assets/a1b69426-8742-4cd2-9239-256c81e93d4e" />

In Homepage go to add new item in select pipeline and give a name to it and configure the pipeline with required details , here i am going to run the pipeline from the jenkins files which i have in Git repository by providing my repository url (you bneed to provide credntials if your repo is private in my case it was public ) then the branch to fetch wheter from main or feature branches.then path of the jenkins file where it was located in repo and then save the job.
Now run Build to trigger pipeline in my jenkins 
I have configure four pipelines for four microservices presented.
<img width="1340" height="550" alt="image" src="https://github.com/user-attachments/assets/7a828cfd-9bde-41c7-bb1d-6f6a548d5dc6" />

My jenkins pipeline have added stages to checkoutsource code, install dependencies, testing application, building of application, building dockerimage, and pushing it to dockerhub using provided docker credentials, and updating the build image into kubernetes manifest files which we used for GitOPS to Continous delivery.
<img width="1252" height="212" alt="image" src="https://github.com/user-attachments/assets/55fc17d3-6e33-47e2-b9f0-9081ed253e85" />
Now the new builded image has been updated in the kubernetes manifest files.

Continous Deployment: 
prerequisites for cd: Kubernetes cluster, here im using Azure kubernetes cluster.
configure axure cli and aks installfor kubectl on your local machine or any Virtual machine and logged into kubernetes cluster by using azure cli. in azure cli set up kubernetes cluster through 
<img width="547" height="222" alt="image" src="https://github.com/user-attachments/assets/11b01a8f-1750-418d-9c02-6a1cec0aaeb2" />

you will be logged into yur cluster from there create a namespace with Argocd and install the argocd into that namespace.and to check argocd is installed or not ? do  kubectl get pods -n argocd to check the services use kubectl get svc -n argocd,we have patched argocd server to Loadbalancer to access through browser.so you will get the external address usingservice command you can use that address in order to access through browser.
<img width="1161" height="422" alt="image" src="https://github.com/user-attachments/assets/fcf3f920-cfdf-43a5-8912-2be84d3cf221" />

while accessing Argocd in browser you need credentials to login where 
username: admin 
Password: xxxxxxxxxxxxxxxxxx
you can retrive that password with: kubectl -n argocd get secret argocd-initial-admin-secret
-o jsonpath="{.data.password}" | base64 -d echo 
paste the credentials you will be logged into Argocd homepage
<img width="1335" height="687" alt="image" src="https://github.com/user-attachments/assets/6c52319c-fc0e-4744-8a1a-cbe2e0b839f0" />

In Argocd go to settings go to the repositories added via http and provided git repo url and click on connect Note:my account has been public there was no need of credentials
<img width="1347" height="347" alt="image" src="https://github.com/user-attachments/assets/b5ef6a03-86cf-421e-a8cf-1583cf354d86" />

Now go to Argocd application click on new application then provide application name, projectname, sync policy i have kept as automatic then repo url will be automaticaly visible as we have added in previous step you can select that or you can add your target repo url to deploy the application through argocd. then give the namespace where your application needed to be deployed. add path of the kubernertes manifest files which needs to deploy the application. 
<img width="1315" height="512" alt="image" src="https://github.com/user-attachments/assets/3756e335-d0dd-4e6f-8632-dfadeff8b434" />
Now argocd will deploy the application in your Aks cluster
<img width="1342" height="631" alt="image" src="https://github.com/user-attachments/assets/45fb1670-9dce-43e8-ac11-c4e65c431323" />
Now go to your kubernetes cluster and check whetehr the pods and service are running or not
<img width="902" height="352" alt="image" src="https://github.com/user-attachments/assets/7880d036-3d1c-4bf7-a286-b0308da4d9cc" />
i have changed the application frontend-service to Loadbalancer to expose the application throughout internet using Loadbalancer address we can access the application.with the given external address login to browser
now you can succesfully access the applications microservices and place an ordertoo 
<img width="1346" height="682" alt="image" src="https://github.com/user-attachments/assets/9ed37828-7a6d-4980-9615-c8ea516d0ed7" />
<img width="1337" height="662" alt="image" src="https://github.com/user-attachments/assets/601e07bc-4bd8-4ddf-9b07-e64778cacc32" />


This Project helps me practical experience how to perform Continous integration through Jenkins pipeline and  Continous Deployment through Gitops via Argocd in kubernetes cluster. where in Continous Integration part i have been build pipeline for checkout SRC. building, testing application , and pushing the docker image to dockerhub and updating the latest image in the kubernetes manifest file

In Continous Deployment part we have set up Argocd in kubernetes cluster and added the repo of the updated kubernetes manifest to watch and sync automatically , and deployed those changes in cluster

I have also tested complete automation of the CICD by making the change in application interface for frontend and git commit main branch  which triggered the entire CICD proceess and we can see the newest version of image deployed in kubernetes cluster.








