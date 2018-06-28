import json

from manifest.resource import Resource


def handler(event, context):
    site = event['pathParameters']['site']
    ts = int(event['queryStringParameters']['since'])
    results = []

    for r in Resource.updated_at_idx.query(site, Resource.updated_at > ts):
        results.append(r.url)

    return {
        'statusCode': 200,
        'body': json.dumps({'items': results})
    }
