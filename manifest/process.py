import json
import logging

from manifest.manifest import Manifest
from manifest.resource import Resource

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    site = event['site']
    location = event['location']
    created = 0
    updated = 0

    for resource in process(site, location):
        save = False
        try:
            r = Resource.get(resource.site, resource.url)
            if resource_updated(r, resource):
                save = True
                updated += 1
        except Resource.DoesNotExist:
            save = True
            created += 1

        if save:
            resource.save()

    status = {
        'site': site,
        'message': 'ok',
        'created': created,
        'updated': updated,
    }
    logger.info(json.dumps(status))

    return status


def process(site, location):
    mf = Manifest(site, location)
    if mf.download():
        pass

    return mf.process()


def resource_updated(old, new):
    return new.deleted != old.deleted or new.updated_at > old.updated_at
