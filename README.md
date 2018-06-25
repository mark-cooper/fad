# FAD

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

sls invoke local --function -f process --config=$FAD_CONFIG
sls invoke local --function -f api --config=$FAD_CONFIG

sls deploy --config=$FAD_CONFIG
sls invoke -f process -l --config=$FAD_CONFIG
sls invoke -f api -l --config=$FAD_CONFIG
sls remove --config=$FAD_CONFIG
unset $AWS_PROFILE
```
