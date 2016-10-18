import logging
import uuid

from datetime import datetime
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

import ndb_json
from app_config import config
from domain_model import Domain
from entity_groups import TenantEntityGroup
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
    playlist = ndb.StringProperty(required=False, indexed=True)
    playlist_id = ndb.StringProperty(required=False, indexed=True)
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
    content_manager_display_name = ndb.StringProperty(required=False, indexed=True)
    content_manager_location_description = ndb.StringProperty(required=False, indexed=True)
    location_key = ndb.KeyProperty(required=False, indexed=True)
    timezone = ndb.StringProperty(required=False, indexed=True)
    timezone_offset = ndb.IntegerProperty(required=False, indexed=True)  # computed property
    registration_correlation_identifier = ndb.StringProperty(required=False, indexed=True)
    archived = ndb.BooleanProperty(default=False, required=True, indexed=True)
    panel_sleep = ndb.BooleanProperty(default=False, required=True, indexed=True)
    overlays_available = ndb.BooleanProperty(default=False, required=True, indexed=True)
    controls_mode = ndb.StringProperty(required=False, indexed=True, default='invisible')
    orientation_mode = ndb.StringProperty(required=False, indexed=True, default='invisible')
    class_version = ndb.IntegerProperty()

    def get_tenant(self):
        if self.tenant_key:
            return self.tenant_key.get()
        else:
            logging.debug(
                'Device has no tenant. Most likely an unmanaged device where tenant has not been specified.')
            return None

    @property
    def overlays(self):
        return OverlayTemplate.create_or_get_by_device_key(self.key)

    @property
    def overlays_as_dict(self):
        """ This method is offered because restler doesn't support keyProperty serialization beyond a single child"""
        json = ndb_json.dumps(self.overlays)
        python_dict = ndb_json.loads(json)
        if "device_key" in python_dict:
            del python_dict["device_key"]
        for key, value in python_dict.iteritems():
            if key != "key":
                if python_dict[key]:
                    # Player team wants the positional key to also be in a field called "gravity"
                    python_dict[key]["gravity"] = key
                    if python_dict[key]["type"] == "logo":
                        python_dict[key]["name"] = python_dict[key]["image_key"]["name"]
                        del python_dict[key]["image_key"]["tenant_key"]
                        python_dict[key]["imageKey"] = python_dict[key]["image_key"]
                        del python_dict[key]["image_key"]
                    else:
                        python_dict[key]["name"] = python_dict[key]["type"]
                        if python_dict[key]["name"] == None:
                            python_dict[key]["name"] = "none"

        return python_dict

    def enable_overlays(self):
        self.overlays_available = True
        self.put()

    @classmethod
    def get_by_device_id(cls, device_id):
        if device_id:
            chrome_os_device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.archived == False,
                                                                ChromeOsDevice.device_id == device_id)).get(
                keys_only=True)
            if chrome_os_device_key:
                return chrome_os_device_key.get()

    @classmethod
    def create_managed(cls,
                       gcm_registration_id,
                       mac_address,
                       tenant_key=None,
                       ethernet_mac_address=None,
                       device_id=None,
                       serial_number=None,
                       archived=False,
                       model=None,
                       timezone=config.DEFAULT_TIMEZONE,
                       registration_correlation_identifier=None):
        timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
        proof_of_play_editable = False
        if tenant_key:
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
            playlist='****initial playlist****',
            playlist_id='****initial playlist id****',
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES,
            timezone=timezone,
            timezone_offset=timezone_offset,
            proof_of_play_editable=proof_of_play_editable,
            registration_correlation_identifier=registration_correlation_identifier)
        return device

    @classmethod
    def create_unmanaged(cls,
                         gcm_registration_id,
                         mac_address,
                         timezone=config.DEFAULT_TIMEZONE,
                         registration_correlation_identifier=None):
        timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
        device = cls(
            archived=False,
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
            playlist='****initial playlist****',
            playlist_id='****initial playlist id****',
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES,
            timezone=timezone,
            timezone_offset=timezone_offset,
            proof_of_play_editable=False,
            registration_correlation_identifier=registration_correlation_identifier,
            model='unmanaged device',
            serial_number='no serial number')
        return device

    @classmethod
    def get_by_gcm_registration_id(cls, gcm_registration_id):
        if gcm_registration_id:
            results = ChromeOsDevice.query(ChromeOsDevice.gcm_registration_id == gcm_registration_id,
                                           ndb.AND(ChromeOsDevice.archived == False)).fetch()
            return results
        else:
            return None

    @classmethod
    def get_by_serial_number(cls, serial_number):
        if serial_number:
            results = ChromeOsDevice.query(ChromeOsDevice.serial_number == serial_number).fetch()
            return results[0] if results else  None  # there should never be multiple multiple serials in this query
        else:
            return None

    @classmethod
    def get_by_mac_address(cls, mac_address):
        if mac_address:
            results = ChromeOsDevice.query(
                ndb.OR(ChromeOsDevice.mac_address == mac_address,
                       ChromeOsDevice.ethernet_mac_address == mac_address),
                ndb.AND(ChromeOsDevice.archived == False)).fetch()
            return results
        else:
            return None

    @classmethod
    def get_by_pairing_code(cls, pairing_code):
        if pairing_code:
            results = ChromeOsDevice.query(ChromeOsDevice.pairing_code == pairing_code,
                                           ndb.AND(ChromeOsDevice.archived == False)).fetch()
            return results
        else:
            return None

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
    def mac_address_already_assigned(cls, device_mac_address, is_unmanaged_device=False):
        mac_address_already_assigned_to_device = ChromeOsDevice.query(
            ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                   ChromeOsDevice.ethernet_mac_address == device_mac_address),
            ndb.AND(
                ChromeOsDevice.is_unmanaged_device == is_unmanaged_device,
                ChromeOsDevice.archived == False)).count() > 0
        return mac_address_already_assigned_to_device

    @classmethod
    def gcm_registration_id_already_assigned(cls, gcm_registration_id, is_unmanaged_device=False):
        gcm_registration_id_already_assigned_to_device = ChromeOsDevice.query(
            ndb.AND(ChromeOsDevice.gcm_registration_id == gcm_registration_id,
                    ChromeOsDevice.is_unmanaged_device == is_unmanaged_device)).count() > 0
        return gcm_registration_id_already_assigned_to_device

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


#####################################################
# DEVICE ISSUE LOG
#####################################################
@ae_ndb_serializer
class DeviceIssueLog(ndb.Model):
    device_key = ndb.KeyProperty(kind=ChromeOsDevice, required=True, indexed=True)
    category = ndb.StringProperty(required=True, indexed=True)
    up = ndb.BooleanProperty(default=True, required=False, indexed=True)
    program = ndb.StringProperty(required=False, indexed=True)
    program_id = ndb.StringProperty(required=False, indexed=True)
    last_error = ndb.StringProperty(required=False, indexed=True)
    playlist = ndb.StringProperty(required=False, indexed=True)
    playlist_id = ndb.StringProperty(required=False, indexed=True)
    storage_utilization = ndb.IntegerProperty(default=0, required=True, indexed=True)
    memory_utilization = ndb.IntegerProperty(default=0, required=True, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    level = ndb.IntegerProperty(default=0, required=True, indexed=True)
    level_descriptor = ndb.StringProperty(default='normal', required=True, indexed=True)
    resolved = ndb.BooleanProperty(default=False, required=True, indexed=True)
    resolved_datetime = ndb.DateTimeProperty(required=False, auto_now=False, indexed=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def create(cls,
               device_key,
               category,
               up=True,
               storage_utilization=0,
               memory_utilization=0,
               program=None,
               program_id=None,
               last_error=None,
               playlist=None,
               playlist_id=None,
               resolved=False,
               resolved_datetime=None):
        if category in [config.DEVICE_ISSUE_MEMORY_HIGH, config.DEVICE_ISSUE_STORAGE_LOW]:
            level = 1
            level_descriptor = 'Warning'
        elif category in [config.DEVICE_ISSUE_PLAYER_DOWN]:
            level = 2
            level_descriptor = 'Danger'
        else:
            level = 0
            level_descriptor = 'Normal'
        return cls(device_key=device_key,
                   category=category,
                   up=up,
                   storage_utilization=storage_utilization,
                   memory_utilization=memory_utilization,
                   program=program,
                   program_id=program_id,
                   last_error=last_error,
                   playlist=playlist,
                   playlist_id=playlist_id,
                   resolved=resolved,
                   resolved_datetime=resolved_datetime,
                   level=level,
                   level_descriptor=level_descriptor)

    @classmethod
    def no_matching_issues(cls, device_key, category, up=True, storage_utilization=0, memory_utilization=0,
                           program=None):
        issues = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                      ndb.AND(DeviceIssueLog.category == category),
                                      ndb.AND(DeviceIssueLog.storage_utilization == storage_utilization),
                                      ndb.AND(DeviceIssueLog.memory_utilization == memory_utilization),
                                      ndb.AND(DeviceIssueLog.up == up),
                                      ndb.AND(DeviceIssueLog.program == program),
                                      ndb.AND(DeviceIssueLog.resolved == False)
                                      ).get(keys_only=True)
        return None == issues

    @classmethod
    def device_not_reported_yet(cls, device_key):
        issues = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key).get(keys_only=True)
        return None == issues

    @classmethod
    def get_all_by_device_key(cls, device_key):
        return DeviceIssueLog.query(DeviceIssueLog.device_key == device_key).fetch()

    @classmethod
    def device_has_unresolved_memory_issues(cls, device_key):
        return cls._has_unresolved_issues(device_key, config.DEVICE_ISSUE_MEMORY_HIGH)

    @classmethod
    def device_has_unresolved_storage_issues(cls, device_key):
        return cls._has_unresolved_issues(device_key, config.DEVICE_ISSUE_STORAGE_LOW)

    @classmethod
    def resolve_device_down_issues(cls, device_key, resolved_datetime):
        cls._resolve_device_issue(device_key, config.DEVICE_ISSUE_PLAYER_DOWN, resolved_datetime)

    @classmethod
    def resolve_device_memory_issues(cls, device_key, resolved_datetime):
        cls._resolve_device_issue(device_key, config.DEVICE_ISSUE_MEMORY_HIGH, resolved_datetime)

    @classmethod
    def resolve_device_storage_issues(cls, device_key, resolved_datetime):
        cls._resolve_device_issue(device_key, config.DEVICE_ISSUE_STORAGE_LOW, resolved_datetime)

    @staticmethod
    def _has_unresolved_issues(device_key, category):
        issues = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                      ndb.AND(DeviceIssueLog.category == category),
                                      ndb.AND(DeviceIssueLog.resolved == False),
                                      ndb.AND(DeviceIssueLog.resolved_datetime == None)).get(keys_only=True)
        return False if issues is None else True

    @staticmethod
    def _resolve_device_issue(device_key, category, resolved_datetime):
        issues = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                      ndb.AND(DeviceIssueLog.device_key == device_key),
                                      ndb.AND(DeviceIssueLog.category == category),
                                      ndb.AND(DeviceIssueLog.resolved == False),
                                      ndb.AND(DeviceIssueLog.resolved_datetime == None)).fetch()
        for issue in issues:
            issue.up = True
            issue.resolved = True
            if category in [config.DEVICE_ISSUE_MEMORY_HIGH, config.DEVICE_ISSUE_STORAGE_LOW]:
                issue.level = 1
                issue.level_descriptor = 'Warning'
            elif category in [config.DEVICE_ISSUE_PLAYER_DOWN]:
                issue.level = 2
                issue.level_descriptor = 'Danger'
            else:
                issue.level = 0
                issue.level_descriptor = 'Normal'
            issue.resolved_datetime = resolved_datetime
            issue.put()

    @staticmethod
    def _resolve_device_issue(device_key, category, resolved_datetime):
        issues = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                      ndb.AND(DeviceIssueLog.device_key == device_key),
                                      ndb.AND(DeviceIssueLog.category == category),
                                      ndb.AND(DeviceIssueLog.resolved == False),
                                      ndb.AND(DeviceIssueLog.resolved_datetime == None)).fetch()
        for issue in issues:
            issue.up = True
            issue.resolved = True
            if category in [config.DEVICE_ISSUE_MEMORY_HIGH, config.DEVICE_ISSUE_STORAGE_LOW]:
                issue.level = 1
                issue.level_descriptor = 'Warning'
            elif category in [config.DEVICE_ISSUE_PLAYER_DOWN]:
                issue.level = 2
                issue.level_descriptor = 'Danger'
            else:
                issue.level = 0
                issue.level_descriptor = 'Normal'
            issue.resolved_datetime = resolved_datetime
            issue.put()

    def _pre_put_hook(self):
        self.class_version = 1


#####################################################
# TENANT AND LOCATION
#####################################################
@ae_ndb_serializer
class Tenant(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    tenant_code = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    admin_email = ndb.StringProperty(required=True)
    content_server_url = ndb.StringProperty(required=True)
    content_manager_base_url = ndb.StringProperty(required=False)
    chrome_device_domain = ndb.StringProperty()
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)
    domain_key = ndb.KeyProperty(kind=Domain, required=True, indexed=True)
    notification_emails = ndb.StringProperty(repeated=True, indexed=False, required=False)
    proof_of_play_logging = ndb.BooleanProperty(default=False, required=True, indexed=True)
    proof_of_play_url = ndb.StringProperty(required=False)
    default_timezone = ndb.StringProperty(required=True, indexed=True, default=config.DEFAULT_TIMEZONE)
    enrollment_email = ndb.StringProperty(required=False, indexed=True)
    enrollment_password = ndb.StringProperty(required=False, indexed=False)
    organization_unit_id = ndb.StringProperty(required=False, indexed=True)
    organization_unit_path = ndb.StringProperty(required=False, indexed=True)
    overlays_available = ndb.BooleanProperty(default=False, required=False, indexed=True)
    overlays_update_in_progress = ndb.BooleanProperty(default=False, required=False, indexed=True)
    class_version = ndb.IntegerProperty()

    @property
    def devices(self, unmanaged=True, managed=True, archived=False):
        if unmanaged and managed:
            return ChromeOsDevice.query(ChromeOsDevice.tenant_key == self.key,
                                        ChromeOsDevice.archived == archived).fetch()
        elif unmanaged and not managed:
            return ChromeOsDevice.query(ChromeOsDevice.tenant_key == self.key,
                                        ChromeOsDevice.is_unmanaged_device == True,
                                        ChromeOsDevice.archived == archived).fetch()
        elif managed and not managed:
            return ChromeOsDevice.query(ChromeOsDevice.tenant_key == self.key,
                                        ChromeOsDevice.is_unmanaged_device == False,
                                        ChromeOsDevice.archived == archived).fetch()
        else:
            raise ValueError("You must choose either an unmanaged player, a managed player, or both.")

    def gcm_update_devices(self, host, user_identifier, devices=None, deferred_call=True):
        from device_message_processor import change_intent
        if not devices:
            devices = self.devices
        for each_device in devices:
            if deferred_call:
                deferred.defer(
                    change_intent,
                    gcm_registration_id=each_device.gcm_registration_id,
                    payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                    device_urlsafe_key=each_device.key.urlsafe(),
                    host=host,
                    user_identifier=user_identifier
                )
            else:
                change_intent(
                    gcm_registration_id=each_device.gcm_registration_id,
                    payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                    device_urlsafe_key=each_device.key.urlsafe(),
                    host=host,
                    user_identifier=user_identifier)

    @property
    def overlays(self):
        return OverlayTemplate.create_or_get_by_tenant_key(self.key)

    @property
    def overlays_as_dict(self):
        """ This method is offered because restler doesn't support keyProperty serialization beyond a single child"""
        json = ndb_json.dumps(self.overlays)
        python_dict = ndb_json.loads(json)
        if "device_key" in python_dict:
            del python_dict["device_key"]
        if "tenant_key" in python_dict:
            del python_dict["tenant_key"]
        for key, value in python_dict.iteritems():
            if key != "key":
                if python_dict[key]:
                    # Player team wants the positional key to also be in a field called "gravity"
                    python_dict[key]["gravity"] = key
                    if python_dict[key]["type"] == "logo":
                        python_dict[key]["name"] = python_dict[key]["image_key"]["name"]
                        del python_dict[key]["image_key"]["tenant_key"]
                        python_dict[key]["imageKey"] = python_dict[key]["image_key"]
                        del python_dict[key]["image_key"]
                    else:
                        python_dict[key]["name"] = python_dict[key]["type"]
                        if python_dict[key]["name"] == None:
                            python_dict[key]["name"] = "none"

        return python_dict

    def get_domain(self):
        return self.domain_key.get()

    @classmethod
    def create(cls,
               tenant_code,
               name,
               admin_email,
               content_server_url,
               domain_key,
               active,
               content_manager_base_url,
               notification_emails=[],
               overlays_available=False,
               proof_of_play_logging=False,
               proof_of_play_url=config.DEFAULT_PROOF_OF_PLAY_URL,
               default_timezone=config.DEFAULT_TIMEZONE,
               ou_create=False):

        if ou_create:
            try:
                domain = ndb.Key(urlsafe=domain_key.urlsafe()).get()
            except Exception, e:
                logging.exception(e)
            if domain.organization_unit_path:
                organization_unit_path = '{0}/{1}'.format(domain.organization_unit_path, tenant_code)
            else:
                organization_unit_path = '/skykit/{0}'.format(tenant_code)
            enrollment_password = cls.generate_enrollment_password(config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE)
            enrollment_email = 'en.{0}@{1}'.format(tenant_code, domain_key.get().name)
        else:
            organization_unit_path = None
            enrollment_password = None
            enrollment_email = None

        tenant_entity_group = TenantEntityGroup.singleton()
        return cls(parent=tenant_entity_group.key,
                   tenant_code=tenant_code,
                   name=name,
                   admin_email=admin_email,
                   content_server_url=content_server_url,
                   domain_key=domain_key,
                   active=active,
                   overlays_available=overlays_available,
                   content_manager_base_url=content_manager_base_url,
                   notification_emails=notification_emails,
                   proof_of_play_logging=proof_of_play_logging,
                   proof_of_play_url=proof_of_play_url,
                   default_timezone=default_timezone,
                   enrollment_password=enrollment_password,
                   enrollment_email=enrollment_email,
                   organization_unit_path=organization_unit_path)

    @staticmethod
    def generate_enrollment_password(length):
        if not isinstance(length, int) or length < config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE:
            raise ValueError('enrollment_password must be greater than {0} in length'.format(
                config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_SIZE - 1))
        chars = config.ACCEPTABLE_ENROLLMENT_USER_PASSWORD_CHARS
        from os import urandom
        return ''.join([chars[ord(c) % len(chars)] for c in urandom(length)])

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Tenant.query(Tenant.name == name).get(keys_only=True)
            if key:
                return key.get()

    @classmethod
    def tenants_of_distributor(cls, distributor_urlsafe_key):
        distributor = ndb.Key(urlsafe=distributor_urlsafe_key)
        domain_keys = Domain.query(Domain.distributor_key == distributor).fetch(100, keys_only=True)
        tenant_list = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        tenant_list = filter(lambda x: x.active, tenant_list)
        result = filter(lambda x: x.domain_key in domain_keys, tenant_list)
        sorted_result = sorted(result, key=lambda k: k.tenant_code)
        return sorted_result

    @classmethod
    def find_by_partial_name_across_all_distributors(cls, partial_name):
        all_tenants = Tenant.query().fetch()
        return [item for item in all_tenants if partial_name.lower() in item.name.lower()]

    @classmethod
    def find_by_partial_name(cls, partial_name, distributor_urlsafe_key):
        all_tenants_of_distributor = cls.tenants_of_distributor(distributor_urlsafe_key)
        return [item for item in all_tenants_of_distributor if partial_name.lower() in item.name.lower()]

    @classmethod
    def find_by_tenant_code(cls, tenant_code):
        tenant_entity = Tenant.query(Tenant.tenant_code == tenant_code, Tenant.active == True).fetch()
        if tenant_entity:
            return tenant_entity[0]
        else:
            return None

    @classmethod
    def find_by_organization_unit_path(cls, organization_unit_path):
        tenant = Tenant.query(Tenant.organization_unit_path == organization_unit_path,
                              Tenant.active == True).fetch()
        if tenant:
            return tenant[0]
        else:
            organization_unit_path_components = organization_unit_path.split('/')
            last_index = len(organization_unit_path_components) - 1
            if organization_unit_path[0][0] == '/':  # leading forward slash
                for i in range(1, last_index):
                    if organization_unit_path_components[i].lower() == 'skykit':
                        if organization_unit_path_components[i + 1]:
                            tenant_code = organization_unit_path_components[i + 1].lower()
                            tenant = Tenant.find_by_tenant_code(tenant_code)
                            break
            else:
                for i in range(0, last_index):  # no leading forward slash
                    if organization_unit_path_components[i].lower() == 'skykit':
                        if organization_unit_path_components[i + 1]:
                            tenant_code = organization_unit_path_components[i + 1].lower()
                            tenant = Tenant.find_by_tenant_code(tenant_code)
                            break

        return tenant

    @classmethod
    def is_tenant_code_unique(cls, tenant_code):
        return not Tenant.query(Tenant.tenant_code == tenant_code).get(keys_only=True)

    @classmethod
    def find_devices(cls, tenant_key, unmanaged=False):
        if tenant_key:
            return ChromeOsDevice.query(
                ndb.AND(ChromeOsDevice.archived == False,
                        ChromeOsDevice.tenant_key == tenant_key,
                        ChromeOsDevice.is_unmanaged_device == unmanaged)
            ).fetch()

    @classmethod
    def find_devices_with_partial_serial(cls, tenant_keys, unmanaged, partial_serial):
        q = ChromeOsDevice.query(ChromeOsDevice.archived == False).filter(
            ChromeOsDevice.tenant_key.IN(tenant_keys)).filter(
            ChromeOsDevice.is_unmanaged_device == unmanaged).fetch()

        to_return = []

        for item in q:
            if item.serial_number and partial_serial in item.serial_number:
                to_return.append(item)

        return to_return

    @classmethod
    def find_devices_with_partial_mac(cls, tenant_keys, unmanaged, partial_mac):
        q = ChromeOsDevice.query(ChromeOsDevice.archived == False). \
            filter(ChromeOsDevice.tenant_key.IN(tenant_keys)).filter(
            ChromeOsDevice.is_unmanaged_device == unmanaged).fetch()

        filtered_results = []

        for item in q:
            appended_already = False
            if item.ethernet_mac_address:
                if partial_mac in item.ethernet_mac_address:
                    filtered_results.append(item)
                    appended_already = True

            if not appended_already:
                if item.mac_address:
                    if partial_mac in item.mac_address:
                        filtered_results.append(item)

        return filtered_results

    @classmethod
    def find_devices_with_partial_gcmid(cls, tenant_keys, unmanaged, partial_gcmid):
        q = ChromeOsDevice.query(ChromeOsDevice.archived == False).filter(
            ChromeOsDevice.tenant_key.IN(tenant_keys)).filter(
            ChromeOsDevice.is_unmanaged_device == unmanaged).fetch()

        filtered_devices = []

        for item in q:
            if (item.gcm_registration_id and partial_gcmid in item.gcm_registration_id) or (
                        item.gcm_registration_id and item.gcm_registration_id == partial_gcmid):
                filtered_devices.append(item)

        return filtered_devices

    ################################################
    # FIND DEVICES OF DISTRIBUTOR
    ################################################
    @classmethod
    def find_devices_with_partial_mac_of_distributor(cls, distributor_urlsafe_key, unmanaged, partial_mac):
        domain_tenant_list = cls.tenants_of_distributor(distributor_urlsafe_key)
        tenant_keys = [tenant.key for tenant in domain_tenant_list]
        return cls.find_devices_with_partial_mac(tenant_keys, unmanaged, partial_mac)

    @classmethod
    def find_devices_with_partial_serial_of_distributor(cls, distributor_urlsafe_key, unmanaged, partial_serial):
        domain_tenant_list = cls.tenants_of_distributor(distributor_urlsafe_key)
        tenant_keys = [tenant.key for tenant in domain_tenant_list]
        return cls.find_devices_with_partial_serial(tenant_keys, unmanaged, partial_serial)

    @classmethod
    def find_devices_with_partial_gcmid_of_distributor(cls, distributor_urlsafe_key, unmanaged, partial_gcmid):
        domain_tenant_list = cls.tenants_of_distributor(distributor_urlsafe_key)
        tenant_keys = [tenant.key for tenant in domain_tenant_list]
        return cls.find_devices_with_partial_gcmid(tenant_keys, unmanaged, partial_gcmid)

    ################################################
    # FIND DEVICES GLOBALLY (ADMIN SEARCH)
    ################################################
    @classmethod
    def find_devices_with_partial_mac_globally(cls, unmanaged, partial_mac):
        domain_tenant_list = Tenant.query().fetch()
        tenant_keys = [tenant.key for tenant in domain_tenant_list]
        return cls.find_devices_with_partial_mac(tenant_keys, unmanaged, partial_mac)

    @classmethod
    def find_devices_with_partial_serial_globally(cls, unmanaged, partial_serial):
        domain_tenant_list = Tenant.query().fetch()
        tenant_keys = [tenant.key for tenant in domain_tenant_list]
        return cls.find_devices_with_partial_serial(tenant_keys, unmanaged, partial_serial)

    @classmethod
    def find_devices_with_partial_gcmid_globally(cls, unmanaged, partial_gcmid):
        domain_tenant_list = Tenant.query().fetch()
        tenant_keys = [tenant.key for tenant in domain_tenant_list]
        return cls.find_devices_with_partial_gcmid(tenant_keys, unmanaged, partial_gcmid)

    ################################################
    @classmethod
    def find_issues_paginated(cls, start, end, device, fetch_size=25, prev_cursor_str=None,
                              next_cursor_str=None):
        objects = None
        next_cursor = None
        prev_cursor = None

        if not prev_cursor_str and not next_cursor_str:
            objects, next_cursor, more = DeviceIssueLog.query(
                DeviceIssueLog.device_key == device.key,
                ndb.AND(DeviceIssueLog.created > start),
                ndb.AND(DeviceIssueLog.created <= end)
            ).order(
                -DeviceIssueLog.created
            ).fetch_page(fetch_size)

            prev_cursor = None
            next_cursor = next_cursor.urlsafe() if more else None

        elif next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            objects, next_cursor, more = DeviceIssueLog.query(
                DeviceIssueLog.device_key == device.key,
                ndb.AND(DeviceIssueLog.created > start),
                ndb.AND(DeviceIssueLog.created <= end)
            ).order(
                -DeviceIssueLog.created
            ).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor
            )

            prev_cursor = next_cursor_str
            next_cursor = next_cursor.urlsafe() if more else None

        elif prev_cursor_str:
            cursor = Cursor(urlsafe=prev_cursor_str)
            objects, prev, more = DeviceIssueLog.query(
                DeviceIssueLog.device_key == device.key,
                ndb.AND(DeviceIssueLog.created > start),
                ndb.AND(DeviceIssueLog.created <= end)
            ).order(
                DeviceIssueLog.created
            ).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor.reversed()
            )

            # needed because we are using a reverse cursor
            objects.reverse()

            next_cursor = prev_cursor_str
            prev_cursor = prev.urlsafe() if more else None

        to_return = {
            'objects': objects or [],
            'next_cursor': next_cursor,
            'prev_cursor': prev_cursor,
        }

        return to_return

    @classmethod
    def find_devices_paginated(cls, tenant_keys, fetch_size=25, unmanaged=False, prev_cursor_str=None,
                               next_cursor_str=None):
        objects = None
        next_cursor = None
        prev_cursor = None

        no_tenant_keys = len(tenant_keys) == 0
        if no_tenant_keys:
            return {
                'objects': objects or [],
                'next_cursor': next_cursor,
                'prev_cursor': prev_cursor,
            }

        if not prev_cursor_str and not next_cursor_str:
            objects, next_cursor, more = ChromeOsDevice.query(
                ndb.OR(ChromeOsDevice.archived == None, ChromeOsDevice.archived == False),
                ndb.AND(
                    ChromeOsDevice.tenant_key.IN(tenant_keys),
                    ChromeOsDevice.is_unmanaged_device == unmanaged)).order(-ChromeOsDevice.created).order(
                ChromeOsDevice.key).fetch_page(
                page_size=fetch_size)

            prev_cursor = None
            next_cursor = next_cursor.urlsafe() if more else None

        elif next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            objects, next_cursor, more = ChromeOsDevice.query(
                ndb.OR(ChromeOsDevice.archived == None, ChromeOsDevice.archived == False),
                ndb.AND(
                    ChromeOsDevice.tenant_key.IN(tenant_keys),
                    ChromeOsDevice.is_unmanaged_device == unmanaged)).order(-ChromeOsDevice.created).order(
                ChromeOsDevice.key).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor
            )

            prev_cursor = next_cursor_str
            next_cursor = next_cursor.urlsafe() if more else None

        elif prev_cursor_str:
            cursor = Cursor(urlsafe=prev_cursor_str)
            objects, prev, more = ChromeOsDevice.query(
                ndb.OR(ChromeOsDevice.archived == None, ChromeOsDevice.archived == False),
                ndb.AND(
                    ChromeOsDevice.tenant_key.IN(tenant_keys),
                    ChromeOsDevice.is_unmanaged_device == unmanaged)).order(ChromeOsDevice.created).order(
                -ChromeOsDevice.key).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor.reversed()
            )

            objects.reverse()
            next_cursor = prev_cursor_str
            prev_cursor = prev.urlsafe() if more else None

        to_return = {
            'objects': objects or [],
            'next_cursor': next_cursor,
            'prev_cursor': prev_cursor,

        }

        return to_return

    @classmethod
    def find_locations_of_tenant_paginated(cls,
                                           tenant_key,
                                           fetch_size=25,
                                           prev_cursor_str=None,
                                           next_cursor_str=None):
        objects = None
        next_cursor = None
        prev_cursor = None

        if not prev_cursor_str and not next_cursor_str:
            objects, next_cursor, more = Location.query(Location.tenant_key == tenant_key).order(
                Location.customer_location_name).order(Location.key).fetch_page(
                page_size=fetch_size
            )

            prev_cursor = None
            next_cursor = next_cursor.urlsafe() if more else None

        elif next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            objects, next_cursor, more = Location.query(Location.tenant_key == tenant_key).order(
                Location.customer_location_name).order(Location.key).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor
            )

            prev_cursor = next_cursor_str
            next_cursor = next_cursor.urlsafe() if more else None

        elif prev_cursor_str:
            cursor = Cursor(urlsafe=prev_cursor_str)
            objects, prev, more = Location.query(Location.tenant_key == tenant_key).order(
                -Location.customer_location_name).order(-Location.key).fetch_page(
                page_size=fetch_size,
                start_cursor=cursor.reversed()
            )

            objects.reverse()

            next_cursor = prev_cursor_str
            prev_cursor = prev.urlsafe() if more else None

        to_return = {
            'objects': objects or [],
            'next_cursor': next_cursor,
            'prev_cursor': prev_cursor,

        }

        return to_return

    @classmethod
    def get_impersonation_email(cls, urlsafe_tenant_key):
        if urlsafe_tenant_key:
            tenant = ndb.Key(urlsafe=urlsafe_tenant_key).get()
            urlsafe_domain_key = tenant.domain_key.urlsafe()
            domain = ndb.Key(urlsafe=urlsafe_domain_key).get()
            return domain.impersonation_admin_email_address

    @classmethod
    def toggle_proof_of_play_on_tenant_devices(cls, should_be_enabled, tenant_code, tenant_key=None):
        if tenant_key:
            tenant = tenant_key.get()
        else:
            tenant = Tenant.find_by_tenant_code(tenant_code)
        managed_devices = Tenant.find_devices(tenant.key, unmanaged=False)
        for device in managed_devices:
            if not should_be_enabled:
                device.proof_of_play_logging = False
            device.proof_of_play_editable = should_be_enabled
            device.put()
        tenant.proof_of_play_logging = should_be_enabled

    @classmethod
    def set_proof_of_play_options(cls, tenant_code, proof_of_play_logging, proof_of_play_url, tenant_key=None):
        if tenant_key:
            tenant = tenant_key.get()
        else:
            tenant = Tenant.find_by_tenant_code(tenant_code)
        if proof_of_play_logging is not None:
            tenant.proof_of_play_logging = proof_of_play_logging
            Tenant.toggle_proof_of_play_on_tenant_devices(
                should_be_enabled=tenant.proof_of_play_logging,
                tenant_code=tenant.tenant_code,
                tenant_key=tenant_key)
        if proof_of_play_url is None or proof_of_play_url == '':
            tenant.proof_of_play_url = config.DEFAULT_PROOF_OF_PLAY_URL
        else:
            tenant.proof_of_play_url = proof_of_play_url.strip().lower()
        tenant.put()

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class Location(ndb.Model):
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True, indexed=True)
    customer_location_code = ndb.StringProperty(required=True, indexed=True)
    customer_location_name = ndb.StringProperty(required=True, indexed=True)
    address = ndb.StringProperty(required=False, indexed=True)
    city = ndb.StringProperty(required=False, indexed=True)
    state = ndb.StringProperty(required=False, indexed=True)
    postal_code = ndb.StringProperty(required=False, indexed=True)
    geo_location = ndb.GeoPtProperty(required=True, indexed=True)
    dma = ndb.StringProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def create(cls, tenant_key, customer_location_name, customer_location_code):
        geo_location_default = ndb.GeoPt(44.98, -93.27)  # Home plate Target Field
        return cls(tenant_key=tenant_key,
                   customer_location_name=customer_location_name,
                   customer_location_code=customer_location_code,
                   geo_location=geo_location_default)

    @classmethod
    def find_by_customer_location_code(cls, customer_location_code):
        if customer_location_code:
            key = Location.query(Location.customer_location_code == customer_location_code).get(keys_only=True)
            if key:
                return key.get()

    @classmethod
    def find_by_partial_location_name(cls, partial_name, tenant_key):
        all_locations = Location.query(Location.tenant_key == tenant_key).fetch()
        return [item for item in all_locations if partial_name.lower() in item.customer_location_name.lower()]

    @classmethod
    def is_customer_location_code_unique(cls, customer_location_code, tenant_key):
        return not Location.query(
            ndb.AND(Location.customer_location_code == customer_location_code, Location.tenant_key == tenant_key)).get(
            keys_only=True)

    def _pre_put_hook(self):
        self.class_version = 1


#####################################################
# OVERLAYS
#####################################################
@ae_ndb_serializer
class Image(ndb.Model):
    filepath = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True)

    @property
    def gcs_path(self):
        return self.tenant_key.get().tenant_code + "/" + self.name

    @staticmethod
    def exists_within_tenant(tenant_key, name):
        return Image.query(ndb.AND(Image.tenant_key == tenant_key, Image.name == name)).fetch()

    @staticmethod
    def create(filepath, name, tenant_key):
        if not Image.exists_within_tenant(tenant_key, name):
            image = Image(
                filepath=filepath,
                name=name,
                tenant_key=tenant_key
            )
            image.put()
            return image
        else:
            raise ValueError("This filename already exists in this tenant")

    @staticmethod
    def get_by_tenant_key(tenant_key):
        return Image.query(Image.tenant_key == tenant_key).fetch()

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class Overlay(ndb.Model):
    type = ndb.StringProperty(indexed=True, required=False)
    size = ndb.StringProperty(indexed=True, required=False)
    # an overlay is optionally associated with an image
    image_key = ndb.KeyProperty(kind=Image, required=False)

    @staticmethod
    def create_or_get(overlay_type, size=None, image_urlsafe_key=None):
        size_options = ["large", "small"]
        if size:
            if (size.lower() not in size_options) and (overlay_type.lower() != "logo"):
                raise ValueError("Overlay size must be in {}".format(size_options))

        # not an overlay with an image that doesn't have a image_urlsafe_key
        if overlay_type and overlay_type.lower() == "logo":
            if image_urlsafe_key == None:
                raise ValueError("You must provide an image_key if you are creating an overlay logo")

        if image_urlsafe_key:
            image_key = ndb.Key(urlsafe=image_urlsafe_key).get().key
        else:
            image_key = None

        overlay_query = Overlay.query(
            ndb.AND(Overlay.type == overlay_type, Overlay.image_key == image_key, Overlay.size == size)).fetch()

        if overlay_query:
            overlay = overlay_query[0]

        # this type of overlay (or type and logo combination) has not been created yet
        else:
            overlay = Overlay(
                type=overlay_type.lower() if overlay_type else overlay_type,
                image_key=image_key,
                size=size.lower() if size else size
            )

            overlay.put()

        return overlay


@ae_ndb_serializer
class OverlayTemplate(ndb.Model):
    top_left = ndb.KeyProperty(kind=Overlay, required=False)
    top_right = ndb.KeyProperty(kind=Overlay, required=False)
    bottom_left = ndb.KeyProperty(kind=Overlay, required=False)
    bottom_right = ndb.KeyProperty(kind=Overlay, required=False)
    # an OverlayTemplate may be associated with either a device or a tenant
    # you should never associate an OverlayTemplate with both a device and a tenant at the same time
    device_key = ndb.KeyProperty(kind=ChromeOsDevice, required=False)
    tenant_key = ndb.KeyProperty(kind=Tenant, required=False)

    def image_in_use(self, image_key):
        in_use_dict = {
            "top_left": False,
            "top_right": False,
            "bottom_left": False,
            "bottom_right": False
        }

        top_left = self.top_left.get()
        if top_left:
            top_left_image = top_left.image_key
            if top_left_image:
                if top_left_image.get().key == image_key:
                    in_use_dict["top_left"] = True

        top_right = self.top_right.get()
        if top_right:
            top_right_image = top_right.image_key
            if top_right_image:
                if top_right_image.get().key == image_key:
                    in_use_dict["top_right"] = True

        bottom_left = self.bottom_left.get()
        if bottom_left:
            bottom_left_image = bottom_left.image_key
            if bottom_left_image:
                if bottom_left_image.get().key == image_key:
                    in_use_dict["bottom_left"] = True

        bottom_right = self.bottom_right.get()
        if bottom_right:
            bottom_right_image = bottom_right.image_key
            if bottom_right_image:
                if bottom_right_image.get().key == image_key:
                    in_use_dict["bottom_right"] = True

        return in_use_dict

    @staticmethod
    # plural, but will always return the 0th index since we are only supporting one template per device for now
    def __get_overlay_template_for_device(device_key):
        overlay_template = OverlayTemplate.query(OverlayTemplate.device_key == device_key).fetch()

        if not overlay_template:
            overlay_template = None
        else:
            overlay_template = overlay_template[0]

        return overlay_template

    @staticmethod
    def create_or_get_by_device_key(device_key):
        existing_template = OverlayTemplate.__get_overlay_template_for_device(device_key)
        if existing_template:
            return existing_template

        else:
            nullOverlay = Overlay.create_or_get(None)
            overlay_template = OverlayTemplate(
                tenant_key=None,
                device_key=device_key,
                top_left=nullOverlay.key,
                top_right=nullOverlay.key,
                bottom_left=nullOverlay.key,
                bottom_right=nullOverlay.key
            )
            overlay_template.put()
            return overlay_template

    @staticmethod
    def __get_overlay_template_for_tenant(tenant_key):
        overlay_template = OverlayTemplate.query(OverlayTemplate.tenant_key == tenant_key).fetch()

        if not overlay_template:
            overlay_template = None
        else:
            overlay_template = overlay_template[0]

        return overlay_template

    @staticmethod
    def create_or_get_by_tenant_key(tenant_key):
        existing_template = OverlayTemplate.__get_overlay_template_for_tenant(tenant_key)
        if existing_template:
            return existing_template

        else:
            nullOverlay = Overlay.create_or_get(None)
            overlay_template = OverlayTemplate(
                device_key=None,
                tenant_key=tenant_key,
                top_left=nullOverlay.key,
                top_right=nullOverlay.key,
                bottom_left=nullOverlay.key,
                bottom_right=nullOverlay.key
            )
            overlay_template.put()
            return overlay_template

    # expects a a dictionary with config about overlay
    def set_overlay(self, position, overlay_type, size=None, image_urlsafe_key=None):
        overlay = Overlay.create_or_get(overlay_type=overlay_type, size=size, image_urlsafe_key=image_urlsafe_key)

        if position.lower() == "top_left":
            self.top_left = overlay.key
            self.put()

        elif position.lower() == "bottom_left":
            self.bottom_left = overlay.key
            self.put()

        elif position.lower() == "bottom_right":
            self.bottom_right = overlay.key
            self.put()

        elif position.lower() == "top_right":
            self.top_right = overlay.key
            self.put()

    def apply_overlay_template_to_all_tenant_devices(self, host, user_identifier, as_deferred=True,
                                                     calledRecursivly=False):
        if as_deferred and not calledRecursivly:
            deferred.defer(self.apply_overlay_template_to_all_tenant_devices, host, user_identifier,
                           calledRecursivly=True)
        else:
            from device_message_processor import change_intent

            if not self.tenant_key:
                raise ValueError(
                    "This OverlayTemplate is not associated with a tenant_key. {}".format(self.key.urlsafe()))
            else:
                tenant_entity = self.tenant_key.get()
                tenant_entity.overlays_update_in_progress = True
                tenant_entity.put()
                tenant_overlay_template = OverlayTemplate.create_or_get_by_tenant_key(tenant_entity.key)
                tenant_devices = tenant_entity.devices

                for device in tenant_devices:
                    device_overlay_template = OverlayTemplate.create_or_get_by_device_key(device.key)
                    device_modified = False

                    if device.overlays_available != tenant_entity.overlays_available:
                        device.overlays_available = tenant_entity.overlays_available
                        device_modified = True

                    if device_overlay_template.top_left.get().key != tenant_overlay_template.top_left.get().key:
                        device_overlay_template.top_left = tenant_overlay_template.top_left
                        device_modified = True

                    if device_overlay_template.top_right.get().key != tenant_overlay_template.top_right.get().key:
                        device_overlay_template.top_right = tenant_overlay_template.top_right
                        device_modified = True

                    if device_overlay_template.bottom_left.get().key != tenant_overlay_template.bottom_left.get().key:
                        device_overlay_template.bottom_left = tenant_overlay_template.bottom_left
                        device_modified = True

                    if device_overlay_template.bottom_right.get().key != tenant_overlay_template.bottom_right.get().key:
                        device_overlay_template.bottom_right = tenant_overlay_template.bottom_right
                        device_modified = True

                    if device_modified:
                        device_overlay_template.put()
                        device.put()

                        change_intent(
                            gcm_registration_id=device.gcm_registration_id,
                            payload=config.PLAYER_UPDATE_DEVICE_REPRESENTATION_COMMAND,
                            device_urlsafe_key=device.key.urlsafe(),
                            host=host,
                            user_identifier=user_identifier)

                tenant_entity.overlays_update_in_progress = False
                tenant_entity.put()
