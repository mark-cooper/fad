# FAD

Finding Aid Depository [AWS Lambda](#) functions.

## Overview

A FAD deployment creates a [DynamoDB](#) table and functions for a single site.
Each site is associated with a manifest: a list of EAD resources and where to
access them online (optionally protected by HTTP basic auth).

## Config

- site: a unique site code
- location: url to manifest csv
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
export TDATA=./test/demo.json

sls plugin install -n serverless-python-requirements

# TODO: setup DDB local
sls invoke local --function -f process -p $TDATA
sls invoke local --function -f api -p $TDATA

sls deploy
sls invoke -f process -l -p $TDATA
sls invoke -f api -l -p $TDATA
sls remove
unset $AWS_PROFILE
```
