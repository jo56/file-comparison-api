#How to run locally
1. Make sure you have python 3.13 installed and configured. You can use pyenv to configure what version of python you have installed for the repo directory
2. Make sure you have pipenv installed and configred. If you do not have pipenv instlled, try running the command <pip install pipenv>
3. Once pipenv is successfully install, run pipenv sync to ensure the packages will work properly
4. Run pipenv shell in the repo directory
5. In the pipenv shell, run the command <uvicorn src.main:app --reload>. You should see a message  Uvicorn running on http://127.0.0.1:8000. This means that the API is running locally
6. You should be able to verify the api is running locally by going to http://127.0.0.1:8000/ in your browser. If successful, you'll see the resonse payload of {
"Sucessful": "Connection"
}
The primary prupose of this api is to use the /compare endpoint to compare two files and detect changes within the ocntents of the files. It supports .py, .txt, .pdf, and .ts, and can allow comparison between files with two difference extensions\
\

#Prod Checklist \
#Deployment
1. The repo already includes code mainitng a CI/CD workflow for deploying the API as an ECS task in AWS. To ensure that the deployments run successfully, follow these steps
  Update your repo's secret values to include the proper AWS creds
2. Set up infrastructe in AWS. Though updating these should be automatic on push, you'll still need to make sure that that the AWS inra is set up in the first place. Configure the following infra using he names provided in the 'deploy.yml' file. Feel free to consult for AWS docs as for how to set these up. You should be able to use th eexisitng resources to fill parameters when creating these services. Create the first go arounds for this infa in this order\
   a. Cloudwatch log group \
   b. ECR Repository \
   c. ECS Task Definition \
   d. ECS Service Cluster \
   e. ECS Service \
   f. Load Balancer (Can be created as a part of the ECS Service setup) \
   g. Configure route 53 to use a custom domain if you don't want to hit the default load balancer\
   You can create all of htese automatically using terraform if you're willing to learn its setup. Otherwise, it shouldn't be too easy to set up manually \
After creating all of this infra and configuring github secrets, you should be able to access the endpoint in a deployed setting by hitting the DNS name instead of http://127.0.0.1:8000. In addition, subsequent commits to the main branch should automatically trigger redpeloyments

#Testing\
These are alreayd unittests that 
#Observability\
The load balancer trgetr group should will be automatically pining the /health endpoint on a successful deployment, which allows us insight into the current healht status of the ECS deployment. This can be further configured to ping alerts depending on the current health status of the deployment. In addition, logging on the ECS level and within the container gives us visibility into what is going on within the service\
#Resiliency\
ECS autocscales the tasks it is running for a service, so a random glitch causing the API tas to fail should just cause another ECS task to be spun up in its place, ensuring that the API won't be down for long. If you were to try to scale up this service, it would be recommended to create multiple ECS services that could act as potnetial backups in case something happens to the main service. CI/CD for these additional services would be easy as you can just use the existing .yml file and change the parameters to this additional service. It could also be worth looking into terraform as a way to automatically deploy all of the infrastructure needed to get the CI/CD pipeline working. This would prevent downtime in a situation where a large amount of the AWS infrasturcture itself gets deleted
#Security\
#Disaster Recovery\
Fortunately this endpoint does not need to worry about long term storage for the files it is comparing. The existing infrastructue should be able to be shut down and spun up again on a whim if deemed necessary. However, if this were to be updated to start storing files, the database setup it should be stored in should have safeguards incorporated to ensure that the data will not me 
