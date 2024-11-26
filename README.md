#How to run locally
1. Make sure you have python 3.13 installed and configured. You can use pyenv to configure what version of python you have installed for the repo directory
2. Make sure you have pipenv installed and configred. If you do not have pipenv instlled, try running the command <pip install pipenv>
3. Once pipenv is successfully install, run pipenv sync to ensure the packages will work properly
4. Run pipenv shell in the repo directory
5. In the pipenv shell, run the command <uvicorn src.main:app --reload>. You should see a message  Uvicorn running on http://127.0.0.1:8000. This means that the API is running locally
6. You should be able to verify the api is running locally by going to http://127.0.0.1:8000/ in your browser. If successful, you'll see the resonse payload of {
"Sucessful": "Connection"
}

#How to run in production
1. The repo already includes code mainitng a CI/CD workflow for deploying the API as an ECS task in AWS. To ensure that the deployments run successfully, follow these steps
  Update your repo's secret values to include the proper AWS creds
2. Set up infrastructe in AWS. Though updating these should be automatic on push, you'll still need to make sure that that the AWS inra is set up in the first place. Configure the following infra using he names provided in the 'deploy.yml' file. Feel free to consult for AWS docs as for how to set these up. You should be able to use th eexisitng resources to fill parameters when creating these services. Create the first go arounds for this infa in this order\
  a. ECR Repository \
  b. ECS Task Definition \
  c. ECS Service Cluster \
  d. ECS Service \
  e. Load Balancer (Can be created as a part of the ECS Service setup) \
  f. Configure route 53 to use a custom domain if you don't want to hit the default load balancer
4. After creating all of this infra and configuring github secrets, you should be able to access the endpoint in a deployed setting by hitting the DNS name instead of http://127.0.0.1:8000

#Additional Prod Checklist Stuff
