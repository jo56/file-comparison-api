The primary prupose of this api is to use the ```/compare_files``` endpoint to compare two files and detect changes within the contents of the files. It supports ```.py```, ```.txt```, ```.pdf```, and ```.ts```, and can allow comparison between files with two different extensions

# How to run locally
1. Make sure you have Python 3.13 installed and configured. You can use ```pyenv``` to configure what version of python you have installed for the repo directory on your machine
2. Make sure you have pipenv installed and configred. If you do not have pipenv installed, try running the command ```pip install pipenv```
3. Once pipenv is successfully installed, run ```pipenv sync``` to ensure the packages will work properly
4. Run ```pipenv shell``` in the repo directory. You should see a shell activate in your directory
5. In the pipenv shell, run the command ```uvicorn src.main:app --reload```. You should see a message  ``Uvicorn running on http://127.0.0.1:8000``. This means that the API is running locally
6. You should be able to verify the api is running locally by going to http://127.0.0.1:8000/ in your browser. If successful, you'll see the resonse payload of ```{
"Sucessful": "Connection"
}```



# Prod Checklist 

## Deployment
The repo already includes for code maintaining a CI/CD workflow for deploying the API as an ECS task in AWS. To ensure that the deployment runs successfully, follow these steps:
  1. Update your repo's secret values to include proper AWS creds
  2. Set up the following infrastructure in AWS. Though updating these should be automatic on push, you'll still need to make sure that that the AWS infra is set up in the first place. Configure the following infra using the names provided in the ```deploy.yml``` file. Feel free to consult for AWS docs as for how to set these up. You should be able to use the exisitng resources to fill parameters when creating these services. 
     
   Create the first go arounds for this infa in this order: \
   a. Cloudwatch log group \
   b. ECR Repository \
   c. ECS Task Definition \
   d. ECS Service Cluster \
   e. ECS Service \
   f. Load Balancer (Can be created as a part of the ECS Service setup) \
   g. (Optional) Configure route 53 to use a custom domain if you don't want to hit the default load balancer
   
   You can create all of these automatically using terraform if you're willing to learn its setup. Otherwise, it shouldn't be too hard to set up manually 

After creating all of this infra and configuring github secrets, you should be able to access the endpoint in a deployed setting by hitting the DNS name of the load balancer (or custom domain if you so choose) instead of http://127.0.0.1:8000. In addition, subsequent commits to the main branch should automatically trigger redpeloyments

## Testing
These are already unit tests that are included as a part of this repo, which are configured to automatically run on each commit. If you were to expand this testing into a prod setting, it could be worth setting up an integration tests for testing the process of actually hitting the API endpoint, intead of just testing the logic that happens when the API is hit.  

## Observability
The load balancer target group should be automatically pinging the ```/health``` endpoint on a successful deployment, which allows us insight into the current health status of the ECS deployment. This can be further configured to send alerts depending on the current health status of the deployment. In addition, logging on the ECS level and within the container gives us visibility into what is going on within the service

## Resiliency
ECS autoscales the tasks it is running for a service, so a random glitch causing the API task to fail should just cause another ECS task to be spun up in its place, ensuring that the API won't be down for long. If you were to try to scale up this service, it would be recommended to create multiple ECS services that could act as potential backups in case something happens to the main service. CI/CD for these additional services would be easy as you can just use the existing ```deploy.yml``` file and change the parameters to this additional service. It could also be worth looking into terraform as a way to automatically deploy all of the infrastructure needed to get the CI/CD pipeline working. This would prevent downtime in a situation where a large amount of the AWS infrasturcture itself gets deleted 

## Security
The load balancer connection by default will use HTTP for its connection. For best security practices, look into Amazon Certificate Manager and use a certificate while configuring the load balancer to ensure the connection is using HTTPS. It is also recommended to add a security measure to the endpoint itself, ensuring that the endpoint can only be hit if one has a proper credential like a bearer token. There is also the precaution to  make sure that different users' files are not accidentally shared with each other. Right now the lack of client-facing logging and lack of in memory storage means that this is less serious of a concern. However, any attempt to store the data beyond the immediate request should be properly secured. 

## Disaster Recovery
Fortunately this endpoint does not need to worry about long term storage for the files it is comparing. The existing infrastructue should be able to be shut down and spun up again on a whim if deemed necessary. However, if this were to be updated to start storing files, the setup for storing the files should have safeguards incorporated to ensure that the data will not me. This was also covered under resiliency, but using a terrform setup to automatically deploy all of the relevant infrastructure on the chance that the existing infra is deleted somehow. This could allow one to spin up all of the important infrasture with one command, allowing the CI/CD process within this repo to continue smoothly
