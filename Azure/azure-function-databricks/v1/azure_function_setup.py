1) create a function app in azure portal
-- use appropriare hosting plan 
-- consumption plan is the cheapest with lowest cost with some latency 


2) Install VS Code 
-- you cannot create functions in the Azure portal, if you have selected Linux VM and Python runtime
-- thus install VS code 
-- install Azure Functions plugin in VS code


3) Make sure you have Azure-cli and Azure functions core tools install and set up


4) create a directory in your local as functions project directory


5) create a function
-- Conside you are using latest V2 model for functions - this creates new folder structure.


# Create a new function from the blob trigger template
>>> func new --name triggerDatabricksJob --template "Blob trigger"
OR for interative way 


>>> func new
-- this creates below folder structure 
dummy2-function-app/
├── .venv/
├── function_app.py
├── host.json
├── local.settings.json
└── requirements.txt



6) update requirements.txt with required packages 
azure-functions
requests 

-- install those using pip install


7) local.settings.json
    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=learn101sankar;AccountKey=+AtdygzvxIil9gQ6JQlepe51wrZE8q628qm91C+AStu1RaSQ==;EndpointSuffix=core.windows.net",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "DatabricksToken": "dapi89286473e1c38f97326ff933d306f",
        "DatabricksWorkspaceUrl": "https://dbc-29254c3-0fad.cloud.databricks.com",
        "DatabricksJobId": "640283835883821"
      }
    }


8) host.json 
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  }
}



9) start the Azure functions - 
>>> func start 

to kill the process 
find PID, and kill 

>>> lsof -i:7071
>>> kill -9 <PID>



10) deploy the functions - 
>>> az login
>>> func azure functionapp publish dummy2

if you want to add variables in the functions - 
>>> az functionapp config appsettings set --name dummy2 --resource-group sankar_learn --settings FUNCTIONS_WORKER_RUNTIME=python FUNCTIONS_EXTENSION_VERSION=~4 WEBSITE_RUN_FROM_PACKAGE=1

WEBSITE_RUN_FROM_PACKAGE 
-- This setting tells Azure to pull your code from a compressed package and run it, which is more reliable than direct file system deployments, especially for Python apps

