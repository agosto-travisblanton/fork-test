from models import (Tenant, ChromeOsDevice, Distributor, Display)
from restler.serializers import ModelStrategy

TENANT_FIELDS = [
    'name',
    'tenant_code',
    'admin_email',
    'content_server_url',
    'chrome_device_domain',
    'active',
    'created',
    'updated'
]
TENANT_STRATEGY = ModelStrategy(Tenant) + TENANT_FIELDS
TENANT_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
]

DISTRIBUTOR_FIELDS = [
    'name',
    'active',
    'created',
    'updated'
]
DISTRIBUTOR_STRATEGY = ModelStrategy(Distributor) + DISTRIBUTOR_FIELDS
DISTRIBUTOR_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
]

CHROME_OS_DEVICE_FIELDS = [
    'device_id',
    'gcm_registration_id',
    'api_key',
    'serial_number',
    'created',
    'updated'
]
CHROME_OS_DEVICE_STRATEGY = ModelStrategy(ChromeOsDevice) + CHROME_OS_DEVICE_FIELDS
CHROME_OS_DEVICE_STRATEGY += [
    {'key': lambda chrome_os_device, field_name, context: chrome_os_device.key.urlsafe()},
    {'tenant': lambda chrome_os_device, field_name, context: chrome_os_device.key.parent().get()}
]

DISPLAY_FIELDS = [
    'device_id',
    'gcm_registration_id',
    'api_key',
    'serial_number',
    'mac_address',
    'managed_display',
    'created',
    'updated',
    'status',
    'last_sync',
    'kind',
    'ethernet_mac_address',
    'org_unit_path',
    'annotated_user',
    'annotated_location',
    'notes',
    'boot_mode',
    'last_enrollment_time',
    'platform_version',
    'model',
    'os_version',
    'firmware_version'
]

DISPLAY_STRATEGY = ModelStrategy(Display) + DISPLAY_FIELDS
DISPLAY_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'tenant': lambda o, field_name, context: o.tenant_key.get()}
]
