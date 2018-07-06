import boto3
import requests

from manifest.resource import Resource
client = boto3.client('ssm')


def handler(event, context):
    site = event['pathParameters']['site']
    url = event['queryStringParameters']['url']
    username = get_secret('fad_' + site + '_username')
    password = get_secret('fad_' + site + '_password')

    # defaults for url not founnd in table
    status = 404
    text = 'Resource not found!'

    try:
        Resource.get(site, url)
        response = requests.get(url, auth=(username, password))
        if response.ok:
            status = response.status_code
            text = response.text
    except Resource.DoesNotExist:
        pass

    return {
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/xml',
        },
        'body': text,
    }


def get_secret(key):
    resp = client.get_parameter(
        Name=key,
        WithDecryption=True
    )
    return resp['Parameter']['Value']
