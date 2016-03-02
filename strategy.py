from datetime import datetime
from google.appengine.ext import ndb

from models import (Tenant, ChromeOsDevice, Distributor, Domain, DeviceIssueLog, PlayerCommandEvent, Location)
from restler.serializers import ModelStrategy
from utils.datetime_util import elapsed_time_message, convert_timezone

TENANT_FIELDS = [
    'name',
    'tenant_code',
    'admin_email',
    'content_server_url',
    'content_manager_base_url',
    'proof_of_play_logging',
    'active',
    'created',
    'updated'
]
TENANT_STRATEGY = ModelStrategy(Tenant) + TENANT_FIELDS
TENANT_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'domain_key': lambda o, field_name, context: o.domain_key.urlsafe() if o.domain_key else None},
    {'notification_emails': lambda o, field_name, context: ', '.join(o.notification_emails).strip(', ')}
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

DEVICE_PAIRING_CODE_STRATEGY = ModelStrategy(ChromeOsDevice)
DEVICE_PAIRING_CODE_STRATEGY += [
    {'pairingCode': lambda o, field_name, context: o.key.get().pairing_code},
    {'gcmRegistrationId': lambda o, field_name, context: o.key.get().gcm_registration_id},
    {'macAddress': lambda o, field_name, context: o.key.get().mac_address}
]

CHROME_OS_DEVICE_STRATEGY = ModelStrategy(ChromeOsDevice)
CHROME_OS_DEVICE_STRATEGY += [
    {'tenantKey': lambda o, field_name, context: o.tenant_key.urlsafe() if o.tenant_key is not None else None},
    {'tenantName': lambda o, field_name, context: o.tenant_key.get().name if o.tenant_key is not None else None},
    {'lastSync': lambda o, field_name, context: o.key.get().last_sync},
    {'apiKey': lambda o, field_name, context: o.key.get().api_key},
    {'macAddress': lambda o, field_name, context: o.key.get().mac_address},
    {'annotatedUser': lambda o, field_name, context: o.key.get().annotated_user},
    {'firmwareVersion': lambda o, field_name, context: o.key.get().firmware_version},
    {'bootMode': lambda o, field_name, context: o.key.get().boot_mode},
    {'chromeDeviceDomain': lambda o, field_name, context: ndb.Key(
        urlsafe=o.tenant_key.get().domain_key.urlsafe()).get().name if o.tenant_key is not None else None},
    {'orgUnitPath': lambda o, field_name, context: o.key.get().org_unit_path},
    {'status': lambda o, field_name, context: o.key.get().status},
    {'updated': lambda o, field_name, context: o.key.get().updated},
    {'tenantCode': lambda o, field_name, context: o.tenant_key.get().tenant_code if o.tenant_key is not None else None},
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
    {'up': lambda o, field_name, context: o.key.get().up},
    {'contentServerUrl': lambda o, field_name,
                                context: o.tenant_key.get().content_server_url if o.tenant_key is not None else None},
    {'model': lambda o, field_name, context: o.key.get().model},
    {'name': lambda o, field_name, context: o.key.get().name},
    {'logglyLink': lambda o, field_name,
                          context: o.key.get().loggly_link if o.key.get().serial_number is not None else None},
    {'etag': lambda o, field_name, context: o.key.get().etag},
    {'isUnmanagedDevice': lambda o, field_name, context: o.key.get().is_unmanaged_device},
    {'pairingCode': lambda o, field_name, context: o.key.get().pairing_code},
    {'panelModel': lambda o, field_name, context: o.key.get().panel_model},
    {'panelInput': lambda o, field_name, context: o.key.get().panel_input},
    {'heartbeatInterval': lambda o, field_name, context: o.key.get().heartbeat_interval_minutes},
    {'checkContentInterval': lambda o, field_name, context: o.key.get().check_for_content_interval_minutes},
    {'connectionType': lambda o, field_name, context: o.key.get().connection_type},
    {'proofOfPlayLogging': lambda o, field_name, context: o.key.get().proof_of_play_logging},
    {'proofOfPlayEditable': lambda o, field_name, context: o.key.get().proof_of_play_editable},
    # Display Location & Timezone information from Location entity:
    {'locationKey': lambda o, field_name, context: o.location_key.urlsafe() if o.location_key is not None else None},
    {'customerLocationCode': lambda o, field_name,
                           context: o.location_key.get().customer_location_code if o.location_key is not None else None},
    {'customerLocationName': lambda o, field_name,
                                  context: o.location_key.get().customer_location_name if o.location_key is not None else None},
    {'customerDisplayCode': lambda o, field_name, context: o.key.get().customer_display_code},
    {'customerDisplayName': lambda o, field_name, context: o.key.get().customer_display_name},
    {'latitude': lambda o, field_name,
                        context: o.location_key.get().geo_location.lat if o.location_key is not None else None},
    {'longitude': lambda o, field_name,
                         context: o.location_key.get().geo_location.lon if o.location_key is not None else None},
    {'timezone': lambda o, field_name, context: o.location_key.get().timezone if o.location_key is not None else None},
    {'timezoneOffset': lambda o, field_name,
                              context: o.location_key.get().timezone_offset if o.location_key is not None else None}
]

LOCATION_STRATEGY = ModelStrategy(Location)
LOCATION_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'tenantKey': lambda o, field_name, context: o.tenant_key.urlsafe() if o.tenant_key is not None else None},
    {'tenantName': lambda o, field_name, context: o.tenant_key.get().name if o.tenant_key is not None else None},
    {'customerLocationCode': lambda o, field_name, context: o.key.get().customer_location_code},
    {'customerLocationName': lambda o, field_name, context: o.key.get().customer_location_name},
    {'timezone': lambda o, field_name, context: o.key.get().timezone},
    {'timezoneOffset': lambda o, field_name, context: o.key.get().timezone_offset},
    {'address': lambda o, field_name, context: o.key.get().address},
    {'city': lambda o, field_name, context: o.key.get().city},
    {'state': lambda o, field_name, context: o.key.get().state},
    {'postalCode': lambda o, field_name, context: o.key.get().postal_code},
    {'latitude': lambda o, field_name,
        context: o.key.get().geo_location.lat if o.key.get().geo_location is not None else None},
    {'longitude': lambda o, field_name,
        context: o.key.get().geo_location.lon if o.key.get().geo_location is not None else None},
    {'dma': lambda o, field_name, context: o.key.get().dma},
    {'created': lambda o, field_name, context: o.key.get().created},
    {'updated': lambda o, field_name, context: o.key.get().updated},
    {'active': lambda o, field_name, context: o.key.get().active}
]

DEVICE_ISSUE_LOG_STRATEGY = ModelStrategy(DeviceIssueLog)
DEVICE_ISSUE_LOG_STRATEGY += [
    {'category': lambda o, field_name, context: o.key.get().category},
    {'up': lambda o, field_name, context: o.key.get().up},
    {'storage_utilization': lambda o, field_name, context: o.key.get().storage_utilization},
    {'memory_utilization': lambda o, field_name, context: o.key.get().memory_utilization},
    {'program': lambda o, field_name, context: o.key.get().program},
    {'created': lambda o, field_name, context: o.key.get().created},
    {'updated': lambda o, field_name, context: o.key.get().updated},
    {'level': lambda o, field_name, context: o.key.get().level},
    {'level_descriptor': lambda o, field_name, context: o.key.get().level_descriptor},
    {'elapsed_time': lambda o, field_name, context: elapsed_time_message(o.key.get().created, datetime.utcnow())}
]

DOMAIN_FIELDS = [
    'name',
    'impersonation_admin_email_address',
    'active',
    'created',
    'updated'
]
DOMAIN_STRATEGY = ModelStrategy(Domain) + DOMAIN_FIELDS
DOMAIN_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'distributor_key': lambda o, field_name, context: o.distributor_key.urlsafe()},

]

PLAYER_COMMAND_EVENT_STRATEGY = ModelStrategy(PlayerCommandEvent)
PLAYER_COMMAND_EVENT_STRATEGY += [
    {'deviceKey': lambda o, field_name, context: o.key.get().device_urlsafe_key},
    {'payload': lambda o, field_name, context: o.key.get().payload},
    {'gcmRegistrationId': lambda o, field_name, context: o.key.get().gcm_registration_id},
    {'postedTime': lambda o, field_name, context: convert_timezone(o.key.get().posted, 'US/Central')},
    {'confirmedTime': lambda o, field_name, context: convert_timezone(o.key.get().confirmed, 'US/Central')},
    {'confirmed': lambda o, field_name, context: o.key.get().player_has_confirmed}
]
