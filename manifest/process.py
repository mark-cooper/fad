import csv
import json
import logging
import os
import requests
import tempfile
import time


from pynamodb.models import Model
from pynamodb.attributes import (
    BooleanAttribute, NumberAttribute, UnicodeAttribute
)


class Manifest:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.file = os.path.join(tempfile.gettempdir(), 'manifest.csv')
        self.date_format = '%Y-%m-%d %H:%M:%S %Z'

    def download(self):
        response = requests.get(self.url)
        if response.ok:
            with open(self.file, 'wb') as f:
                f.write(response.content)
            logging.info('Downloaded and saved manifest: ' + self.file)
            return True
        else:
            raise Exception('Failed to download manifest: ' + self.url)

    def make_resource(self, row):
        # TODO: handle errors
        resource = Resource()
        resource.site = self.name
        resource.url = row['location']

        resource.deleted = True if row.get('deleted', '').lower(
        ) == 'true' else False
        resource.filename = row.get('filename', '')
        resource.title = row.get('title', '')

        if 'updated_at' in row:
            resource.updated_at = time.mktime(
                time.strptime(row['updated_at'], self.date_format)
            )
        else:
            response = requests.head(resource.url)
            if response.ok:
                last_modified = response.headers['Last-Modified']
                resource.updated_at = time.mktime(
                    time.strptime(last_modified, self.date_format)
                )
            else:
                resource.updated_at = time.mktime(time.gmtime(0))
        return resource

    def process(self):
        with open(self.file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, quotechar='"')
            for row in reader:
                resource = self.make_resource(row)
                logging.info('Processing resource: ' + resource.url)
                yield resource


class Resource(Model):
    class Meta:
        table_name = os.getenv('FAD_TABLE_NAME', 'fad')
        region = os.getenv('AWS_REGION')
    site = UnicodeAttribute()
    url = UnicodeAttribute(hash_key=True)
    deleted = BooleanAttribute()
    filename = UnicodeAttribute()
    title = UnicodeAttribute()
    updated_at = NumberAttribute(range_key=True)


def handler(event, context):
    site = os.getenv('MANIFEST_SITE')
    location = os.getenv('MANIFEST_LOCATION')
    created = 0
    updated = 0

    for resource in process(site, location):
        create = False
        count = Resource.count(resource.url)

        if count > 1:
            raise Exception('Duplicate url detected: ' + resource.url)

        if count == 1:
            for r in Resource.query(resource.url, limit=1):
                if resoure_updated(r, resource):
                    r.delete()
                    create = True
                    updated += 1

        if count == 0:
            create = True
            created += 1

        if create:
            resource.save()
            logging.info('Processed: ' + resource.url)

    return {
        'message': 'ok',
        'created': created,
        'updated': updated,
    }


def process(site, location):
    mf = Manifest(site, location)
    if mf.download():
        logging.info('Downloaded manifest: ' + mf.file)

    return mf.process()


def resoure_updated(old, new):
    return new.deleted != old.deleted or new.updated_at > old.updated_at


if __name__ == '__main__':
    demo_data = os.path.join(os.path.dirname(__file__), '../test/demo.json')

    with open(demo_data) as json_data:
        data = json.load(json_data)

    for resource in process(data['site'], data['location']):
        print(json.dumps(resource.__dict__))
