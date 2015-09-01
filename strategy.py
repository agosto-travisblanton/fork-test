from models import (Tenant, ChromeOsDevice, Distributor)
from restler.serializers import ModelStrategy

TENANT_FIELDS = [
    'name',
    'tenant_code',
    'admin_email',
    'content_server_url',
    'chrome_device_domain',
    'domain_key',
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

CHROME_OS_DEVICE_STRATEGY = ModelStrategy(ChromeOsDevice)
CHROME_OS_DEVICE_STRATEGY += [
    {'tenantKey': lambda o, field_name, context: o.tenant_key.urlsafe()},
    {'tenantName': lambda o, field_name, context: o.tenant_key.get().name},
    {'lastSync': lambda o, field_name, context: o.key.get().last_sync},
    {'apiKey': lambda o, field_name, context: o.key.get().api_key},
    {'macAddress': lambda o, field_name, context: o.key.get().mac_address},
    {'annotatedUser': lambda o, field_name, context: o.key.get().annotated_user},
    {'firmwareVersion': lambda o, field_name, context: o.key.get().firmware_version},
    {'bootMode': lambda o, field_name, context: o.key.get().boot_mode},
    {'chromeDeviceDomain': lambda o, field_name, context: o.tenant_key.get().chrome_device_domain},
    {'orgUnitPath': lambda o, field_name, context: o.key.get().org_unit_path},
    {'status': lambda o, field_name, context: o.key.get().status},
    {'updated': lambda o, field_name, context: o.key.get().updated},
    {'tenantCode': lambda o, field_name, context: o.tenant_key.get().tenant_code},
    {'lastEnrollmentTime': lambda o, field_name, context: o.key.get().last_enrollment_time},
    {'ethernetMacAddress': lambda o, field_name, context: o.key.get().ethernet_mac_address},
    {'deviceId': lambda o, field_name, context: o.key.get().device_id},
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'platformVersion': lambda o, field_name, context: o.key.get().platform_version},
    {'osVersion': lambda o, field_name, context: o.key.get().os_version},
    {'annotatedLocation': lambda o, field_name, context: o.key.get().annotated_location},
    {'kind': lambda o, field_name, context: o.key.get().kind},
    {'created': lambda o, field_name, context: o.key.get().created},
    {'notes': lambda o, field_name, context: o.key.get().notes},
    {'serialNumber': lambda o, field_name, context: o.key.get().serial_number},
    {'gcmRegistrationId': lambda o, field_name, context: o.key.get().gcm_registration_id},
    {'contentServerUrl': lambda o, field_name, context: o.tenant_key.get().content_server_url},
    {'model': lambda o, field_name, context: o.key.get().model}
]
