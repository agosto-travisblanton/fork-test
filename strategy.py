from models import (Tenant, ChromeOsDevice)
from restler.serializers import ModelStrategy

TENANT_FIELDS = [
    'name',
    'tenant_code',
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

CHROME_OS_DEVICE_FIELDS = [
    'device_id',
    'gcm_registration_id',
    'created',
    'updated'
]
CHROME_OS_DEVICE_STRATEGY = ModelStrategy(ChromeOsDevice) + CHROME_OS_DEVICE_FIELDS
CHROME_OS_DEVICE_STRATEGY += [
    {'key': lambda chrome_os_device, field_name, context: chrome_os_device.key.urlsafe()},
    {'tenant': lambda chrome_os_device, field_name, context: chrome_os_device.key.parent().get()}
]
