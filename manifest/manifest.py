import csv
import os
import requests
import tempfile
import time

from dateutil import parser
from manifest.resource import Resource


class Manifest:
    def __init__(self, name, url, username='', password=''):
        self.name = name
        self.url = url
        self.file = os.path.join(tempfile.gettempdir(), 'manifest.csv')
        self.username = username
        self.password = password

    def download(self):
        response = requests.get(self.url, auth=(self.username, self.password))
        if response.ok:
            with open(self.file, 'wb') as f:
                f.write(response.content)
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
            resource.updated_at = self.parse_date(row["updated_at"])
        else:
            response = requests.head(
                resource.url, auth=(self.username, self.password)
            )
            if response.ok:
                last_modified = response.headers['Last-Modified']
                resource.updated_at = self.parse_date(last_modified)
            else:
                resource.updated_at = int(time.mktime(time.gmtime(0)))
        return resource

    def parse_date(self, updated_at):
        return int(parser.parse(updated_at).timestamp())

    def process(self):
        with open(self.file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, quotechar='"')
            for row in reader:
                resource = self.make_resource(row)
                yield resource
