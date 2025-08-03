import logging
import os
import json
import requests
import azure.functions as func

# Instantiate the FunctionApp object. This is the entry point for your application.
app = func.FunctionApp()

# The decorator defines the trigger and bindings for this function.
# The 'name' is the function name that will appear in the portal.
# The 'path' specifies the container and file pattern to monitor.
# The 'connection' references the app setting for the storage account connection string.

@app.blob_trigger(arg_name="myblob", path="sqltoblob/{name}", connection="AzureWebJobsStorage")
def triggerDatabricksJob(myblob: func.InputStream):
    """
    Azure Blob Storage trigger function that triggers a Databricks job.

    Args:
        myblob (func.InputStream): The input blob that triggered this function.
    """
    logging.info(f"Python blob trigger function processed blob: {myblob.name}")

    try:
        # Retrieve secrets and configuration from application settings
        # In local development, these are read from local.settings.json
        databricks_token = os.environ["DatabricksToken"]
        databricks_workspace_url = os.environ["DatabricksWorkspaceUrl"]
        databricks_job_id = os.environ["DatabricksJobId"]

        # Construct the API endpoint URL for running a Databricks job immediately
        # We use API 2.1 which is the recommended version for new code.
        api_endpoint = f"{databricks_workspace_url}/api/2.1/jobs/run-now"

        # Define the payload for the API request.
        # The Databricks Jobs API requires the job_id.
        payload = {
            "job_id": int(databricks_job_id)
        }

        # Set up the headers for the API request
        headers = {
            "Authorization": f"Bearer {databricks_token}",
            "Content-Type": "application/json"
        }

        logging.info(f"Triggering Databricks job ID: {databricks_job_id}...")

        # Make the POST request to trigger the job
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Log the successful response from the Databricks API
        response_json = response.json()
        run_id = response_json.get("run_id")
        logging.info(f"Successfully triggered Databricks job. Run ID: {run_id}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error triggering Databricks job: {e}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise e
