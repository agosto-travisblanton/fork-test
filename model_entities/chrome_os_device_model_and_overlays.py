import logging
import uuid
import ndb_json
from datetime import datetime
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
from app_config import config
from restler.decorators import ae_ndb_serializer
from domain_model import Domain
from entity_groups import TenantEntityGroup
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
    overlay_available = ndb.BooleanProperty(default=False, required=True, indexed=True)
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
        return OverlayTemplate.get_overlay_template_for_device(self.key)

    @property
    def overlays_as_dict(self):
        """ This method is offered because restler doesn't support keyProperty serialization beyond a single child"""
        json = ndb_json.dumps(self.overlays)
        return ndb_json.loads(json)

    def enable_overlays(self):
        self.overlay_available = True
        self.put()
        return self

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
                       model=None, timezone='America/Chicago', registration_correlation_identifier=None):
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
                         timezone='America/Chicago',
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
                    ChromeOsDevice.is_unmanaged_device == is_unmanaged_device,
                    ChromeOsDevice.archived == False)).count() > 0
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
    default_timezone = ndb.StringProperty(required=True, indexed=True, default='America/Chicago')
    class_version = ndb.IntegerProperty()

    def get_domain(self):
        return self.domain_key.get()

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Tenant.query(Tenant.name == name).get(keys_only=True)
            if key:
                return key.get()

    @classmethod
    def find_by_partial_name(cls, partial_name):
        # search for all tenants because datastore does not support wildcard searches
        all_tenants = Tenant.query().fetch()
        # returns wildcard matches for partial_name
        return [item for item in all_tenants if partial_name.lower() in item.name.lower()]

    @classmethod
    def find_by_tenant_code(cls, tenant_code):
        if tenant_code:
            tenant_key = Tenant.query(Tenant.tenant_code == tenant_code, Tenant.active == True).get(keys_only=True)
            if tenant_key:
                return tenant_key.get()

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
    def create(cls, tenant_code, name, admin_email, content_server_url, domain_key, active,
               content_manager_base_url, notification_emails=[], proof_of_play_logging=False,
               proof_of_play_url=config.DEFAULT_PROOF_OF_PLAY_URL, default_timezone='America/Chicago'):

        tenant_entity_group = TenantEntityGroup.singleton()

        return cls(parent=tenant_entity_group.key,
                   tenant_code=tenant_code,
                   name=name,
                   admin_email=admin_email,
                   content_server_url=content_server_url,
                   domain_key=domain_key,
                   active=active,
                   content_manager_base_url=content_manager_base_url,
                   notification_emails=notification_emails,
                   proof_of_play_logging=proof_of_play_logging,
                   proof_of_play_url=proof_of_play_url,
                   default_timezone=default_timezone)

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
    def find_by_partial_location_name(cls, partial_name):
        all_locations = Location.query().fetch()
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
    svg_rep = ndb.TextProperty(required=True)
    name = ndb.StringProperty(required=True, indexed=True)
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True)

    @staticmethod
    def exists_within_tenant(tenant_key, name):
        return Image.query(ndb.AND(Image.tenant_key == tenant_key, Image.name == name)).fetch()

    @staticmethod
    def create(svg_rep, name, tenant_key):
        if not Image.exists_within_tenant(tenant_key, name):
            image = Image(
                svg_rep=svg_rep,
                name=name,
                tenant_key=tenant_key
            )
            image.put()
            return image
        else:
            return False

    @staticmethod
    def get_by_tenant_key(tenant_key):
        return Image.query(Image.tenant_key == tenant_key).fetch()

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class Overlay(ndb.Model):
    type = ndb.StringProperty(indexed=True, required=False)
    # an overlay is optionally associated with an image
    image_key = ndb.KeyProperty(kind=Image, required=False)

    @staticmethod
    def create_or_get(overlay_type, image_urlsafe_key=None):
        # not an overlay with an image that doesn't have a image_urlsafe_key
        if overlay_type == "LOGO":
            if image_urlsafe_key == None:
                raise ValueError("You must provide an image_key if you are creating an overlay logo")

        if image_urlsafe_key:
            image_key = ndb.Key(urlsafe=image_urlsafe_key).get().key
        else:
            image_key = None

        overlay_query = Overlay.query(ndb.AND(Overlay.type == overlay_type, Overlay.image_key == image_key)).fetch()

        if overlay_query:
            overlay = overlay_query[0]

        # this type of overlay (or type and logo combination) has not been created yet
        else:
            overlay = Overlay(
                type=overlay_type,
                image_key=image_key
            )

            overlay.put()

        return overlay


@ae_ndb_serializer
class OverlayTemplate(ndb.Model):
    top_left = ndb.KeyProperty(kind=Overlay, required=False)
    top_right = ndb.KeyProperty(kind=Overlay, required=False)
    bottom_left = ndb.KeyProperty(kind=Overlay, required=False)
    bottom_right = ndb.KeyProperty(kind=Overlay, required=False)
    device_key = ndb.KeyProperty(kind=ChromeOsDevice, required=True)

    @staticmethod
    # plural, but will always return the 0th index since we are only supporting one template per device for now
    def get_overlay_template_for_device(device_key):
        overlay_template = OverlayTemplate.query(OverlayTemplate.device_key == device_key).fetch()

        if not overlay_template:
            nullOverlay = Overlay.create_or_get(None)
            overlay_template = OverlayTemplate(
                device_key=device_key,
                top_left=nullOverlay.key,
                top_right=nullOverlay.key,
                bottom_left=nullOverlay.key,
                bottom_right=nullOverlay.key
            )
            overlay_template.put()

        else:
            overlay_template = overlay_template[0]

        return overlay_template

    @staticmethod
    def create_or_get_by_device_key(device_key):
        existing_template = OverlayTemplate.get_overlay_template_for_device(device_key)
        if existing_template:
            return existing_template

        else:
            nullOverlay = Overlay.create_or_get(None)
            overlay_template = OverlayTemplate(
                device_key=device_key,
                top_left=nullOverlay.key,
                top_right=nullOverlay.key,
                bottom_left=nullOverlay.key,
                bottom_right=nullOverlay.key
            )
            overlay_template.put()
            return overlay_template

    # expects a a dictionary with config about overlay
    def set_overlay(self, position, overlay_type, image_urlsafe_key=None):

        overlay = Overlay.create_or_get(overlay_type=overlay_type, image_urlsafe_key=image_urlsafe_key)

        if position.upper() == "TOP_LEFT":
            self.top_left = overlay.key
            self.put()

        elif position.upper() == "BOTTOM_LEFT":
            self.bottom_left = overlay.key
            self.put()

        elif position.upper() == "BOTTOM_RIGHT":
            self.bottom_right = overlay.key
            self.put()

        elif position.upper() == "TOP_RIGHT":
            self.top_right = overlay.key
            self.put()