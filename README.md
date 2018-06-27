# FAD

Finding Aid Depository [AWS Lambda](#) functions.

## Overview

A FAD deployment creates a [DynamoDB](#) table and functions to process
manifests and provide access to resources.

A manifest is a list of EAD resources and where to find them online.

A resource is metadata referring to an EAD file that is publicly available or
optionally protected by HTTP basic auth.

The functions are:

### Process

Process a manifest CSV, add resources (manifest entries) to DynamoDB.

### Check

Check status of resources.

### Api

HTTP/s endpoint for accessing resource/s metadata.

## Quickstart

To get up and running with the dev environment:

```bash
# PYTHON
virtualenv venv --python=python3
source venv/bin/activate
pip3 install -r requirements.txt

# SERVERLESS
export AWS_PROFILE=default # # set aws profile if using env
export TDATA=./test/demo.json

sls plugin install -n serverless-python-requirements

sls deploy
sls invoke -f process -l -p $TDATA
sls invoke -f api -l
sls remove
unset $AWS_PROFILE
```

## Config

Create a `config/$env.yml` (derive from `dev.yml` for an example):

```yml
fad:
  - schedule:
      rate: cron(0 6 * * ? *) # every day, 6 am UTC
      enabled: true # false to disable
      input:
        # REQUIRED: site code
        site: demo
        # REQUIRED: location (url) to manifest
        location: https://archivesspace.lyrasistechnology.org/files/exports/manifest_ead_xml.csv
        # OPTIONAL: basic auth username
        username: abc
        # OPTIONAL: basic auth password
        password: abc123
  - schedule:
      # ...
```
