from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

from app_config import config
from restler.decorators import ae_ndb_serializer
from domain_model import Domain
from chrome_os_device_model import ChromeOsDevice
from device_issue_log_model import DeviceIssueLog
from entity_groups import TenantEntityGroup


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
    def find_by_tenant_code(cls, tenant_code):
        if tenant_code:
            key = Tenant.query(Tenant.tenant_code == tenant_code).get(keys_only=True)
            if key:
                return key.get()

    @classmethod
    def is_tenant_code_unique(cls, tenant_code):
        return not Tenant.query(Tenant.tenant_code == tenant_code).get(keys_only=True)

    @classmethod
    def find_devices(cls, tenant_key, unmanaged):
        if tenant_key:
            return ChromeOsDevice.query(
                ndb.AND(ChromeOsDevice.archived == False,
                        ChromeOsDevice.tenant_key == tenant_key,
                        ChromeOsDevice.is_unmanaged_device == unmanaged)
            ).fetch()

    @classmethod
    def match_device_with_full_mac(cls, tenant_keys, unmanaged, full_mac):
        return ChromeOsDevice.query(ChromeOsDevice.archived == False,
                                    ndb.OR(ChromeOsDevice.mac_address == full_mac,
                                           ChromeOsDevice.ethernet_mac_address == full_mac)).filter(
            ChromeOsDevice.tenant_key.IN(tenant_keys)).filter(
            ChromeOsDevice.is_unmanaged_device == unmanaged).count() > 0

    @classmethod
    def match_device_with_full_serial(cls, tenant_keys, unmanaged, full_serial):
        return ChromeOsDevice.query(ChromeOsDevice.archived == False).filter(
            ChromeOsDevice.tenant_key.IN(tenant_keys)).filter(
            ChromeOsDevice.is_unmanaged_device == unmanaged).filter(
            ChromeOsDevice.serial_number == full_serial).count() > 0

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
                    ChromeOsDevice.is_unmanaged_device == unmanaged)).order(ChromeOsDevice.key).fetch_page(
                page_size=fetch_size)

            prev_cursor = None
            next_cursor = next_cursor.urlsafe() if more else None

        elif next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            objects, next_cursor, more = ChromeOsDevice.query(
                ndb.OR(ChromeOsDevice.archived == None, ChromeOsDevice.archived == False),
                ndb.AND(
                    ChromeOsDevice.tenant_key.IN(tenant_keys),
                    ChromeOsDevice.is_unmanaged_device == unmanaged)).order(ChromeOsDevice.key).fetch_page(
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
                    ChromeOsDevice.is_unmanaged_device == unmanaged)).order(-ChromeOsDevice.key).fetch_page(
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
    def is_customer_location_code_unique(cls, customer_location_code, tenant_key):
        return not Location.query(
            ndb.AND(Location.customer_location_code == customer_location_code, Location.tenant_key == tenant_key)).get(
            keys_only=True)

    def _pre_put_hook(self):
        self.class_version = 1
