# CI/CD Automated Databricks Notebook Deployment and Workflows for DEV/STG/PRD



## Overview

This repo provides an example of how to utilize GitLab CI/CD pipelines to deploy notebooks to a Databricks workspace, and then launch a Databricks Job that points at these notebooks.  

## Notebooks Deployment

- Configure DATABRICKS_HOST and DATABRICKS_TOKEN secrets for your project in GitLab UI.  Be careful with the “Protected” option.  If you only want to expose these variables to protected branches, then you will have to be sure that you make the development branch protected (as well as any other branch that you want to kick off CI/CD pipelines)
- Create a new branch in Git named something like “first_deploy”
- Open the GitLab WebIDE and create a new file named .gitlab-ci.yml   This is where we will put the cicd steps
- Here is an example script to deploy to DEV and PRD.  You could re-use most of this script, just update the DEPLOY_PATH.  
```
stages:          # List of stages for jobs, and their order of execution
 - deploy
 - unit-test
 - integration
 
variables:
 DEPLOY_PATH: /Users/adam.kuchinski@databricks.com/adv-sample-folder/builder-data-pipelines/notebook_gitflow_sample_cicd/
 
dev-deploy:       # This job runs in the deploy stage, which runs first.
 stage: deploy
 image: python:latest
 only:
   refs:
     - development
 script:
   - echo "$DATABRICKS_HOST"
   - echo "Install dependencies"
   - pip install databricks-cli
   - echo "Deploying notebooks to DEV.."
   - databricks workspace import_dir --overwrite ./notebooks $DEPLOY_PATH/DEV/notebooks

```

- Now when you commit and merge your code to the development branch, the pipeline will run and it will deploy the notebooks to the provided DEPLOY_PATH/DEV. 

## Running Tests with Databricks Jobs

- Now that you’ve deployed your notebooks to the DEV location, you can create a Job in Databricks that runs some notebooks in that DEV location.  We will walk through how you would update your CI/CD Pipeline to execute the Job everytime there is a new commit/merge to the development branch.
- In Databricks, browse to the Job that you want to use.  Find the Job ID in the top right corner of the job page.  
- Create a new branch named “first_job” (or work directly on the “development” branch).
- Edit the .gitlab-ci.yml file by putting this new job at the bottom of the file, but update the job_id="..." line with your job id.:

```
#run a databricks job, then monitor until it completes.  Fail the pipeline if result_state!=SUCCESS
#This script can be re-used for other jobs, just need to change the job_id=... line with your databricks job id
dev-unit-test:       # This job runs in the unit-test stage, which runs second.  
  stage: unit-test
  image: python:latest
  only:
    refs:
      - development
  before_script:
    - apt-get -qq update
    - apt-get install -y jq
  script:
    - echo "$DATABRICKS_HOST"
    - echo "Install dependencies"
    - pip install databricks-cli
    - echo "Running unit tests"
    - job_id="1018102697350655"
    - run_id=$( databricks jobs run-now --job-id ${job_id} |  jq -r  '.run_id' )    
    - run_url=$( databricks runs get --run-id ${run_id} |  jq -r  '.run_page_url' ) 
    - echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Launching job via run now API"
    - echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Run URL - $run_url"
    - state=$( databricks runs get --run-id ${run_id} |  jq -r  '.state.life_cycle_state' ) 
    - TERMINAL_RUN_LIFECYCLE_STATES=("TERMINATED" "SKIPPED" "INTERNAL_ERROR")
    - until [[ " ${TERMINAL_RUN_LIFECYCLE_STATES[*]} " =~ " ${state} " ]]; do echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] [Run Id - $run_id] Current run status info - ${state}" ; state=$( databricks runs get --run-id ${run_id}  | jq -r  '.state.life_cycle_state' ); sleep 10; done
    - result_state=$( databricks runs get --run-id ${run_id} |  jq -r  '.state.result_state' ) 
    - echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Job finished with final status - $result_state"
    - err_msg="Exception- Tracked run failed during execution. Please check Databricks UI for run logs"
    - if [[ "${result_state}" != "SUCCESS" ]]; then echo $err_msg; exit 1; fi
```

- Now when you commit and merge your code to the development branch, the pipeline will run and it will execute that Job in Databricks. If the job succeeds, so will the pipeline.  If it fails, the pipeline will fail as well. 

## Next Steps

Take a look at the .gitlab-ci.yml file in this project to see an example of both a DEV and PROD deployment.   

Also take a look at the dbx project.  dbx provides a feature set beyond what has been demonstrated here, but it does require access to that python package and all of its dependencies.  

https://docs.databricks.com/dev-tools/dbx.html
https://github.com/databrickslabs/dbx


***


