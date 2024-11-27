#How to run locally
1. Make sure you have python 3.13 installed and configured. You can use pyenv to configure what version of python you have installed for the repo directory
2. Make sure you have pipenv installed and configred. If you do not have pipenv instlled, try running the command <pip install pipenv>
3. Once pipenv is successfully install, run pipenv sync to ensure the packages will work properly
4. Run pipenv shell in the repo directory
5. In the pipenv shell, run the command <uvicorn src.main:app --reload>. You should see a message  Uvicorn running on http://127.0.0.1:8000. This means that the API is running locally
6. You should be able to verify the api is running locally by going to http://127.0.0.1:8000/ in your browser. If successful, you'll see the resonse payload of {
"Sucessful": "Connection"
}

#Prod Checklist \
#Deployment
1. The repo already includes code mainitng a CI/CD workflow for deploying the API as an ECS task in AWS. To ensure that the deployments run successfully, follow these steps
  Update your repo's secret values to include the proper AWS creds
2. Set up infrastructe in AWS. Though updating these should be automatic on push, you'll still need to make sure that that the AWS inra is set up in the first place. Configure the following infra using he names provided in the 'deploy.yml' file. Feel free to consult for AWS docs as for how to set these up. You should be able to use th eexisitng resources to fill parameters when creating these services. Create the first go arounds for this infa in this order\
   Cloudwatch log group \
   ECR Repository \
   ECS Task Definition \
   ECS Service Cluster \
   ECS Service \
   Load Balancer (Can be created as a part of the ECS Service setup) \
   Configure route 53 to use a custom domain if you don't want to hit the default load balancer
After creating all of this infra and configuring github secrets, you should be able to access the endpoint in a deployed setting by hitting the DNS name instead of http://127.0.0.1:8000. In addition, subsequent commits to the main branch should automatically trigger redpeloyments

#Testing\
These are alreayd unittests that 
#Observability\
The load balancer trgetr group should will be automatically pining the /health endpoint on a successful deployment, which allows us insight into current 
#Resiliency\
#Security\
#Disaster Recovery\
Fortunately this endpoint does not need to worry about long term storage for the files it is comparing. The existing infrastructue should be able to be shut down and spun up again on a whim if deemed necessary. However, if this were to be updated to start storing files, the database setup it should be stored in should have safeguards incorporated to ensure that the data will not me 
