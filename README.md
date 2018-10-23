# FAD

[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)

Finding Aid Depository [AWS Lambda](https://aws.amazon.com/lambda/) functions.

## Overview

A FAD deployment creates a [DynamoDB](https://aws.amazon.com/dynamodb/) table and functions to process
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

### Backup

Backup the FAD database.

## Quickstart

To get up and running with the dev environment:

```bash
# PYTHON
virtualenv venv --python=python3
source venv/bin/activate
pip3 install -r requirements.txt

# SERVERLESS
npm install -g serverless
sls plugin install -n serverless-python-requirements
npm install

AWS_PROFILE=default # set aws profile if using env, or use --aws-profile
TDATA=./test/demo.json

sls deploy
sls invoke -f backup -l
sls invoke -f process -l -p $TDATA

sls invoke -f list -l -d '{ "path": "/dev/demo/resources", "pathParameters": { "site": "demo" }, "queryStringParameters": { "since": 0 } }'
sls invoke -f find -l -d '{ "path": "/dev/demo/resources/find", "pathParameters": { "site": "demo" }, "queryStringParameters": { "url": "https://archivesspace.lyrasistechnology.org/staff/files/exports/LYRASIS_OCONNOR_200.xml" } }'

curl --header "x-api-key: $KEY" https://$id.execute-api.us-west-2.amazonaws.com/dev/demo/resources?since=0 | jq .
curl --header "x-api-key: $KEY" 'https://$id.execute-api.us-west-2.amazonaws.com/dev/demo/resources/find?url=$URL'

sls logs -f process -l
sls remove
```

## Config

Create a `config/$env.yml` (derive from `dev.yml` for an example):

```yml
process:
  - schedule:
      rate: cron(0 6 * * ? *) # every day, 6 am UTC
      enabled: true # false to disable
      input:
        # REQUIRED: site code
        site: demo
        # REQUIRED: location (url) to manifest
        location: https://archivesspace.lyrasistechnology.org/staff/files/exports/manifest_ead_xml.csv
        # OPTIONAL: basic auth username
        username: abc
        # OPTIONAL: basic auth password
        password: abc123
  - schedule:
      # ...
```

## License

The project is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
