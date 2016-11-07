from datetime import datetime
from google.appengine.ext import ndb

from models import (Tenant,
                    ChromeOsDevice,
                    Distributor,
                    Domain,
                    DeviceIssueLog,
                    PlayerCommandEvent,
                    Location,
                    IntegrationEventLog,
                    Image,
                    OverlayTemplate
                    )

from restler.serializers import ModelStrategy
from utils.datetime_util import elapsed_time_message

TENANT_FIELDS = [
    'name',
    'tenant_code',
    'admin_email',
    'content_server_url',
    'content_manager_base_url',
    'proof_of_play_logging',
    'proof_of_play_url',
    'default_timezone',
    'active',
    'enrollment_email',
    'enrollment_password',
    'organization_unit_id',
    'organization_unit_path',
    'created',
    'updated',
]
TENANT_STRATEGY = ModelStrategy(Tenant) + TENANT_FIELDS
TENANT_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'domain_key': lambda o, field_name, context: o.domain_key.urlsafe() if o.domain_key else None},
    {'notification_emails': lambda o, field_name, context: ', '.join(o.notification_emails).strip(', ')},
    {'overlayStatus': lambda o, field_name, context: o.overlays_available},
    {'overlays': lambda o, field_name, context: o.overlays_as_dict if o.overlays_available else None},
    {'overlaysUpdateInProgress': lambda o, field_name, context: o.overlays_update_in_progress}

]

DISTRIBUTOR_FIELDS = [
    'name',
    'active',
    'content_manager_url',
    'player_content_url',
    'created',
    'updated'
]
DISTRIBUTOR_STRATEGY = ModelStrategy(Distributor) + DISTRIBUTOR_FIELDS
DISTRIBUTOR_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
]

DEVICE_PAIRING_CODE_STRATEGY = ModelStrategy(ChromeOsDevice)
DEVICE_PAIRING_CODE_STRATEGY += [
    {'pairingCode': lambda o, field_name, context: o.pairing_code},
    {'gcmRegistrationId': lambda o, field_name, context: o.gcm_registration_id},
    {'macAddress': lambda o, field_name, context: o.mac_address}
]


CHROME_OS_DEVICE_STRATEGY = ModelStrategy(ChromeOsDevice)
CHROME_OS_DEVICE_STRATEGY += [
    {'panelSleep': lambda o, field_name, context: o.panel_sleep if o.panel_sleep is not None else None},
    {'tenantKey': lambda o, field_name, context: o.tenant_key.urlsafe() if o.tenant_key is not None else None},
    {'tenantName': lambda o, field_name, context: o.tenant_key.get().name if o.tenant_key is not None else None},
    {'lastSync': lambda o, field_name, context: o.last_sync},
    {'apiKey': lambda o, field_name, context: o.api_key},
    {'macAddress': lambda o, field_name, context: o.mac_address},
    {'annotatedAssetId': lambda o, field_name, context: o.annotated_asset_id},
    {'annotatedLocation': lambda o, field_name, context: o.annotated_location},
    {'annotatedUser': lambda o, field_name, context: o.annotated_user},
    {'firmwareVersion': lambda o, field_name, context: o.firmware_version},
    {'bootMode': lambda o, field_name, context: o.boot_mode},
    {'chromeDeviceDomain': lambda o, field_name, context: ndb.Key(
        urlsafe=o.tenant_key.get().domain_key.urlsafe()).get().name if o.tenant_key is not None else None},
    {'orgUnitPath': lambda o, field_name, context: o.org_unit_path},
    {'status': lambda o, field_name, context: o.status},
    {'updated': lambda o, field_name, context: o.updated},
    {'tenantCode': lambda o, field_name, context: o.tenant_key.get().tenant_code if o.tenant_key is not None else None},
    {'lastEnrollmentTime': lambda o, field_name, context: o.last_enrollment_time},
    {'ethernetMacAddress': lambda o, field_name, context: o.ethernet_mac_address},
    {'deviceId': lambda o, field_name, context: o.device_id},
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'platformVersion': lambda o, field_name, context: o.platform_version},
    {'osVersion': lambda o, field_name, context: o.os_version},
    {'kind': lambda o, field_name, context: o.kind},
    {'created': lambda o, field_name, context: o.created},
    {'notes': lambda o, field_name, context: o.notes},
    {'serialNumber': lambda o, field_name, context: o.serial_number},
    {'gcmRegistrationId': lambda o, field_name, context: o.gcm_registration_id},
    {'up': lambda o, field_name, context: o.up},
    {'contentServerUrl': lambda o, field_name,
                                context: o.tenant_key.get().content_server_url if o.tenant_key is not None else None},
    {'model': lambda o, field_name, context: o.model},
    {'name': lambda o, field_name, context: o.name},
    {'logglyLink': lambda o, field_name,
                          context: o.loggly_link if o.serial_number is not None else None},
    {'etag': lambda o, field_name, context: o.etag},
    {'isUnmanagedDevice': lambda o, field_name, context: o.is_unmanaged_device},
    {'pairingCode': lambda o, field_name, context: o.pairing_code},
    {'panelModel': lambda o, field_name, context: o.panel_model},
    {'panelInput': lambda o, field_name, context: o.panel_input},
    {'heartbeatInterval': lambda o, field_name, context: o.heartbeat_interval_minutes},
    {'checkContentInterval': lambda o, field_name, context: o.check_for_content_interval_minutes},
    {'connectionType': lambda o, field_name, context: o.connection_type},
    {'proofOfPlayLogging': lambda o, field_name, context: o.proof_of_play_logging},
    {'proofOfPlayEditable': lambda o, field_name, context: o.proof_of_play_editable},
    {'proofOfPlayUrl': lambda o, field_name,
                              context: o.tenant_key.get().proof_of_play_url if o.tenant_key is not None else None},
    # Display Location & Timezone information from Location entity:
    {'locationKey': lambda o, field_name, context: o.location_key.urlsafe() if o.location_key is not None else None},
    {'customerLocationCode': lambda o, field_name,
                                    context: o.location_key.get().customer_location_code if o.location_key is not None else None},
    {'customerLocationName': lambda o, field_name,
                                    context: o.location_key.get().customer_location_name if o.location_key is not None else None},
    {'customerDisplayCode': lambda o, field_name, context: o.customer_display_code},
    {'customerDisplayName': lambda o, field_name, context: o.customer_display_name},
    {'contentManagerDisplayName': lambda o, field_name, context: o.content_manager_display_name},
    {'contentManagerLocationDescription': lambda o, field_name,
                                                 context: o.content_manager_location_description},
    {'registrationCorrelationIdentifier': lambda o, field_name,
                                                 context: o.registration_correlation_identifier},
    {'latitude': lambda o, field_name,
                        context: o.location_key.get().geo_location.lat if o.location_key is not None else None},
    {'longitude': lambda o, field_name,
                         context: o.location_key.get().geo_location.lon if o.location_key is not None else None},
    {'timezone': lambda o, field_name, context: o.timezone},
    {'timezoneOffset': lambda o, field_name, context: o.timezone_offset},
    {'program': lambda o, field_name, context: o.program},
    {'programId': lambda o, field_name, context: o.program_id},
    {'playlist': lambda o, field_name, context: o.playlist},
    {'playlistId': lambda o, field_name, context: o.playlist_id},
    {'lastError': lambda o, field_name, context: o.last_error},
    {'archived': lambda o, field_name, context: o.archived},
    {'controlsMode': lambda o, field_name, context: o.controls_mode},
    {'overlayStatus': lambda o, field_name,
                             context: o.overlays_available},
    {'overlays': lambda o, field_name, context: o.overlays_as_dict if o.overlays_available else None},
    {'orientationMode': lambda o, field_name, context: o.orientation_mode},
    {'sleepController': lambda o, field_name, context: o.sleep_controller}

]

LOCATION_STRATEGY = ModelStrategy(Location)
LOCATION_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'tenantKey': lambda o, field_name, context: o.tenant_key.urlsafe() if o.tenant_key is not None else None},
    {'tenantName': lambda o, field_name, context: o.tenant_key.get().name if o.tenant_key is not None else None},
    {'customerLocationCode': lambda o, field_name, context: o.customer_location_code},
    {'customerLocationName': lambda o, field_name, context: o.customer_location_name},
    {'address': lambda o, field_name, context: o.address},
    {'city': lambda o, field_name, context: o.city},
    {'state': lambda o, field_name, context: o.state},
    {'postalCode': lambda o, field_name, context: o.postal_code},
    {'latitude': lambda o, field_name,
                        context: o.geo_location.lat if o.geo_location is not None else None},
    {'longitude': lambda o, field_name,
                         context: o.geo_location.lon if o.geo_location is not None else None},
    {'dma': lambda o, field_name, context: o.dma},
    {'created': lambda o, field_name, context: o.created},
    {'updated': lambda o, field_name, context: o.updated},
    {'active': lambda o, field_name, context: o.active}
]

DEVICE_ISSUE_LOG_STRATEGY = ModelStrategy(DeviceIssueLog)
DEVICE_ISSUE_LOG_STRATEGY += [
    {'category': lambda o, field_name, context: o.category},
    {'up': lambda o, field_name, context: o.up},
    {'storageUtilization': lambda o, field_name, context: o.storage_utilization},
    {'memoryUtilization': lambda o, field_name, context: o.memory_utilization},
    {'program': lambda o, field_name, context: o.program},
    {'programId': lambda o, field_name, context: o.program_id},
    {'lastError': lambda o, field_name, context: o.last_error},
    {'playlist': lambda o, field_name, context: o.playlist},
    {'playlistId': lambda o, field_name, context: o.playlist_id},
    {'created': lambda o, field_name, context: o.created},
    {'updated': lambda o, field_name, context: o.updated},
    {'level': lambda o, field_name, context: o.level},
    {'levelDescriptor': lambda o, field_name, context: o.level_descriptor},
    {'elapsedTime': lambda o, field_name, context: elapsed_time_message(o.created, datetime.utcnow())}
]

DOMAIN_FIELDS = [
    'name',
    'impersonation_admin_email_address',
    'organization_unit_path',
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
    {'deviceKey': lambda o, field_name, context: o.device_urlsafe_key},
    {'payload': lambda o, field_name, context: o.payload},
    {'gcmRegistrationId': lambda o, field_name, context: o.gcm_registration_id},
    {'userIdentifier': lambda o, field_name, context: o.user_identifier},
    {'postedTime': lambda o, field_name, context: o.posted},
    {'confirmedTime': lambda o, field_name, context: o.confirmed},
    {'confirmed': lambda o, field_name, context: o.player_has_confirmed}
]

INTEGRATION_EVENT_LOG_STRATEGY = ModelStrategy(IntegrationEventLog)
INTEGRATION_EVENT_LOG_STRATEGY += [
    {'eventCategory': lambda o, field_name, context: o.event_category},
    {'correlationIdentifier': lambda o, field_name, context: o.correlation_identifier},
    {'componentName': lambda o, field_name, context: o.component_name},
    {'workflowStep': lambda o, field_name, context: o.workflow_step},
    {'utcTimestamp': lambda o, field_name, context: o.utc_timestamp},
    {'deviceUrlSafeKey': lambda o, field_name, context: o.device_urlsafe_key},
    {'serialNumber': lambda o, field_name, context: o.serial_number},
    {'tenantCode': lambda o, field_name, context: o.tenant_code},
    {'gcmRegistrationId': lambda o, field_name, context: o.gcm_registration_id},
    {'macAddress': lambda o, field_name, context: o.mac_address},
    {'details': lambda o, field_name, context: o.details}
]

IMAGE_STRATEGY = ModelStrategy(Image)
IMAGE_STRATEGY += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'tenant_key': lambda o, field_name, context: o.tenant_key},
    {'name': lambda o, field_name, context: o.name},
    {'svg_rep': lambda o, field_name, context: o.svg_rep},
]

OVERLAY_TEMPLATE = ModelStrategy(OverlayTemplate)
OVERLAY_TEMPLATE += [
    {'key': lambda o, field_name, context: o.key.urlsafe()},
    {'top_right': lambda o, field_name, context: o.top_right.get() if o.top_right else None},
    {'bottom_right': lambda o, field_name, context: o.bottom_right.get() if o.bottom_right else None},
    {'top_left': lambda o, field_name, context: o.top_left.get() if o.top_left else None},
    {'bottom_left': lambda o, field_name, context: o.bottom_left.get() if o.bottom_left else None},

]
