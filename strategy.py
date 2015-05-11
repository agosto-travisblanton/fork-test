from models import (Tenant)
from restler.serializers import ModelStrategy

TENANT_FIELDS = [
    'name',
    'created',
    'updated'
]
TENANT_STRATEGY = ModelStrategy(Tenant) + TENANT_FIELDS
TENANT_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
]

