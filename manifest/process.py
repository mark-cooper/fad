import csv
import json
import logging
import os
import requests
import tempfile
import time


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


class Resource:
    pass


def handler(event, context):
    site = os.getenv('MANIFEST_SITE')
    location = os.getenv('MANIFEST_LOCATION')
    for resource in process(site, location):
        print(json.dumps(resource.__dict__))


def process(site, location):
    mf = Manifest(site, location)
    if mf.download():
        print('Downloaded manifest: ' + mf.file)

    return mf.process()


if __name__ == '__main__':
    demo_data = os.path.join(os.path.dirname(__file__), '../test/demo.json')

    with open(demo_data) as json_data:
        data = json.load(json_data)

    for resource in process(data['site'], data['location']):
        print(resource.title)
