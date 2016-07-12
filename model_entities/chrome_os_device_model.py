import uuid
from datetime import datetime
from google.appengine.ext import ndb
from app_config import config
from restler.decorators import ae_ndb_serializer
from utils.timezone_util import TimezoneUtil


@ae_ndb_serializer
class ChromeOsDevice(ndb.Model):
    tenant_key = ndb.KeyProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    device_id = ndb.StringProperty(required=False, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=True)
    mac_address = ndb.StringProperty(required=True, indexed=True)
    api_key = ndb.StringProperty(required=True, indexed=True)
    serial_number = ndb.StringProperty(required=False, indexed=True)
    status = ndb.StringProperty(required=False, indexed=False)
    last_sync = ndb.StringProperty(required=False, indexed=False)
    kind = ndb.StringProperty(required=False, indexed=False)
    ethernet_mac_address = ndb.StringProperty(required=False, indexed=True)
    org_unit_path = ndb.StringProperty(required=False, indexed=False)
    annotated_user = ndb.StringProperty(required=False, indexed=False)
    annotated_location = ndb.StringProperty(required=False, indexed=False)
    annotated_asset_id = ndb.StringProperty(required=False, indexed=False)
    notes = ndb.StringProperty(required=False, indexed=False)
    boot_mode = ndb.StringProperty(required=False, indexed=False)
    last_enrollment_time = ndb.StringProperty(required=False, indexed=False)
    platform_version = ndb.StringProperty(required=False, indexed=False)
    model = ndb.StringProperty(required=False, indexed=False)
    os = ndb.StringProperty(required=False, indexed=False)
    os_version = ndb.StringProperty(required=False, indexed=False)
    firmware_version = ndb.StringProperty(required=False, indexed=False)
    etag = ndb.StringProperty(required=False, indexed=False)
    name = ndb.ComputedProperty(lambda self: '{0} {1}'.format(self.serial_number, self.model))
    loggly_link = ndb.ComputedProperty(lambda self: 'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(
        self.serial_number))
    is_unmanaged_device = ndb.BooleanProperty(default=False, required=True, indexed=True)
    pairing_code = ndb.StringProperty(required=False, indexed=True)
    panel_model = ndb.StringProperty(required=False, indexed=True)
    panel_input = ndb.StringProperty(required=False, indexed=True)
    heartbeat_updated = ndb.DateTimeProperty(required=False, auto_now=False, indexed=True)
    up = ndb.BooleanProperty(default=True, required=True, indexed=True)
    storage_utilization = ndb.IntegerProperty(default=0, required=True, indexed=True)
    memory_utilization = ndb.IntegerProperty(default=0, required=True, indexed=True)
    program = ndb.StringProperty(required=False, indexed=True)
    program_id = ndb.StringProperty(required=False, indexed=True)
    last_error = ndb.StringProperty(required=False, indexed=True)
    connection_type = ndb.StringProperty(required=False, indexed=True)
    sk_player_version = ndb.StringProperty(required=False, indexed=True)
    heartbeat_interval_minutes = ndb.IntegerProperty(default=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES, required=True,
                                                     indexed=False)
    check_for_content_interval_minutes = ndb.IntegerProperty(default=config.CHECK_FOR_CONTENT_INTERVAL_MINUTES,
                                                             required=True, indexed=True)
    proof_of_play_logging = ndb.BooleanProperty(default=False, required=True, indexed=True)
    proof_of_play_editable = ndb.BooleanProperty(default=False, required=True)
    customer_display_name = ndb.StringProperty(required=False, indexed=True)
    customer_display_code = ndb.StringProperty(required=False, indexed=True)
    location_key = ndb.KeyProperty(required=False, indexed=True)
    timezone = ndb.StringProperty(required=False, indexed=True)
    timezone_offset = ndb.IntegerProperty(required=False, indexed=True)  # computed property
    registration_correlation_identifier = ndb.StringProperty(required=False, indexed=True)
    archived = ndb.BooleanProperty(default=False, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    def get_tenant(self):
        return self.tenant_key.get()

    @classmethod
    def get_by_device_id(cls, device_id):
        if device_id:
            chrome_os_device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.archived == False,
                                                                ChromeOsDevice.device_id == device_id)).get(
                keys_only=True)
            if chrome_os_device_key:
                return chrome_os_device_key.get()

    @classmethod
    def create_managed(cls, tenant_key, gcm_registration_id, mac_address, ethernet_mac_address=None, device_id=None,
                       serial_number=None, archived=False,
                       model=None, timezone='America/Chicago'):
        timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
        proof_of_play_editable = False
        tenant = tenant_key.get()
        if tenant:
            if tenant.proof_of_play_logging:
                proof_of_play_editable = True
        device = cls(
            device_id=device_id,
            archived=archived,
            tenant_key=tenant_key,
            gcm_registration_id=gcm_registration_id,
            mac_address=mac_address,
            ethernet_mac_address=ethernet_mac_address,
            api_key=str(uuid.uuid4().hex),
            serial_number=serial_number,
            model=model,
            is_unmanaged_device=False,
            up=True,
            storage_utilization=0,
            memory_utilization=0,
            heartbeat_updated=datetime.utcnow(),
            program='****initial****',
            program_id='****initial****',
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES,
            timezone=timezone,
            timezone_offset=timezone_offset,
            proof_of_play_editable=proof_of_play_editable)
        return device

    @classmethod
    def create_unmanaged(cls, gcm_registration_id, mac_address, timezone='America/Chicago'):
        timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
        device = cls(
            gcm_registration_id=gcm_registration_id,
            mac_address=mac_address,
            api_key=str(uuid.uuid4().hex),
            pairing_code='{0}-{1}-{2}-{3}'.format(str(uuid.uuid4().hex)[:4], str(uuid.uuid4().hex)[:4],
                                                  str(uuid.uuid4().hex)[:4], str(uuid.uuid4().hex)[:4]),
            is_unmanaged_device=True,
            up=True,
            storage_utilization=0,
            memory_utilization=0,
            heartbeat_updated=datetime.utcnow(),
            program='****initial****',
            program_id='****initial****',
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES,
            timezone=timezone,
            timezone_offset=timezone_offset)
        return device

    @classmethod
    def get_unmanaged_device_by_mac_address(cls, mac_address):
        if mac_address:
            device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.mac_address == mac_address,
                                                      ChromeOsDevice.is_unmanaged_device == True,
                                                      ChromeOsDevice.archived == False)).get(keys_only=True)
            if not device_key:
                return None
            else:
                return device_key.get()
        else:
            return None

    @classmethod
    def get_unmanaged_device_by_gcm_registration_id(cls, gcm_registration_id):
        if gcm_registration_id:
            device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.gcm_registration_id == gcm_registration_id,
                                                      ChromeOsDevice.is_unmanaged_device == True,
                                                      ChromeOsDevice.archived == False)).get(keys_only=True)
            if not device_key:
                return None
            else:
                return device_key.get()
        else:
            return None

    @classmethod
    def mac_address_already_assigned(cls, device_mac_address):
        mac_address_assigned_to_device = ChromeOsDevice.query(
            ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                   ChromeOsDevice.ethernet_mac_address == device_mac_address),
            ndb.AND(ChromeOsDevice.archived == False)).count() > 0
        return mac_address_assigned_to_device

    @classmethod
    def is_rogue_unmanaged_device(cls, mac_address):
        device = ChromeOsDevice.get_unmanaged_device_by_mac_address(mac_address)
        if device is not None and device.pairing_code is not None and device.tenant_key is None:
            return True
        else:
            return False

    @classmethod
    def is_customer_display_code_unique(cls, customer_display_code, tenant_key):
        return None is ChromeOsDevice.query(
            ndb.AND(ChromeOsDevice.archived == False,
                    ChromeOsDevice.customer_display_code == customer_display_code,
                    ChromeOsDevice.tenant_key == tenant_key)).get(
            keys_only=True)

    def _pre_put_hook(self):
        self.class_version = 3

    def get_impersonation_email(self):
        return self.get_tenant().get_domain().impersonation_admin_email_address
