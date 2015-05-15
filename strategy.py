from models import (Tenant)
from restler.serializers import ModelStrategy

TENANT_FIELDS = [
    'name',
    'admin_email',
    'content_server_url',
    'content_server_api_key',
    'chrome_device_domain',
    'active',
    'created',
    'updated'
]
TENANT_STRATEGY = ModelStrategy(Tenant) + TENANT_FIELDS
TENANT_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
]

