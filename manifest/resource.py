import os

from pynamodb.models import Model
from pynamodb.indexes import LocalSecondaryIndex, AllProjection
from pynamodb.attributes import (
    BooleanAttribute, NumberAttribute, UnicodeAttribute
)


class ResourceUpdatedAtIndex(LocalSecondaryIndex):
    class Meta:
        projection = AllProjection()
    site = UnicodeAttribute(hash_key=True)
    updated_at = NumberAttribute(range_key=True)


class Resource(Model):
    class Meta:
        table_name = os.getenv('FAD_TABLE_NAME')
        region = os.getenv('AWS_REGION')
    site = UnicodeAttribute(hash_key=True)
    url = UnicodeAttribute(range_key=True)
    deleted = BooleanAttribute()
    filename = UnicodeAttribute()
    title = UnicodeAttribute()
    updated_at = NumberAttribute()
    updated_at_idx = ResourceUpdatedAtIndex()
