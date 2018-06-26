# FAD

Finding Aid Depository [AWS Lambda](#) functions.

## Overview

A FAD deployment creates a [DynamoDB](#) table and functions for a single site.
Each site is associated with a manifest: a list of EAD resources and where to
access them online (optionally protected by HTTP basic auth).

Each FAD deployment requires a simple `json` configuration file:

```
{
  "location": "https://domain/path/to/manifest.csv",
  "region": "us-west-2",
  "site": "uniquesitecode"
}
```

- location: url to manifest csv
- region: AWS region for function deployment
- site: a unique site code
- username: basic auth username [optional]
- password: basic auth password [optional]

## Functions

### Process

Process a manifest CSV, add resources (manifest entries) to DynamoDB.

### Check

Check status of resources.

### Api

HTTP/s endpoint for accessing resource/s metadata.

## Setup

Python:

```bash
virtualenv venv --python=python3
source venv/bin/activate
pip3 install -r requirements.txt
```

Serverless:

```bash
export AWS_PROFILE=default # # set aws profile if using env
export FAD_CONFIG=./test/demo.json

sls plugin install -n serverless-python-requirements --config=$FAD_CONFIG

# TODO: setup DDB local
sls invoke local --function -f process --config=$FAD_CONFIG
sls invoke local --function -f api --config=$FAD_CONFIG

sls deploy --config=$FAD_CONFIG
sls invoke -f process -l --config=$FAD_CONFIG
sls invoke -f api -l --config=$FAD_CONFIG
sls remove --config=$FAD_CONFIG
unset $AWS_PROFILE
```
