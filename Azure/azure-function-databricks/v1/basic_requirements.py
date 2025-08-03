1) Azure Functions Core Tools (func)
>>> brew tap azure/functions
>>> brew install azure-functions-core-tools@4


2) Azure CLI - 
>>> brew update && brew install azure-cli
Or
>>> pip install azure-cli


3) Resource group name 


4) Azure storage account connection string 


5) Databricks - 
Personal Access Token (PAT) 
databricks_workspace_url
databricks_job_id
api_endpoint = f"{databricks_workspace_url}/api/2.1/jobs/run-now"


6) Azure Storage Account Access Key / SAS Token / Managed Identity - so that databricks can have access to Azure storage files
spark.read.csv("https://<account>.blob.core.windows.net/<container>/<file>?<SAS_TOKEN>")
