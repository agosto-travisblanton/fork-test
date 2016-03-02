import uuid

from datetime import datetime
from google.appengine.ext import ndb

from app_config import config
from restler.decorators import ae_ndb_serializer
from utils.timezone_util import TimezoneUtil

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>. Bob MacNeal <bob.macneal@agosto.com>'

TENANT_ENTITY_GROUP_NAME = 'tenantEntityGroup'
DISTRIBUTOR_ENTITY_GROUP_NAME = 'distributorEntityGroup'


class TenantEntityGroup(ndb.Model):
    name = ndb.StringProperty(required=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def singleton(cls):
        return TenantEntityGroup.get_or_insert(TENANT_ENTITY_GROUP_NAME,
                                               name=TENANT_ENTITY_GROUP_NAME)

    def _pre_put_hook(self):
        self.class_version = 1


class DistributorEntityGroup(ndb.Model):
    name = ndb.StringProperty(required=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def singleton(cls):
        return DistributorEntityGroup.get_or_insert(DISTRIBUTOR_ENTITY_GROUP_NAME,
                                                    name=DISTRIBUTOR_ENTITY_GROUP_NAME)

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class Distributor(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    # TODO Make admin_email required=True after migration run in prod
    admin_email = ndb.StringProperty(required=False, indexed=True)
    player_content_url = ndb.StringProperty(required=False, indexed=True)
    content_manager_url = ndb.StringProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Distributor.query(Distributor.name == name).get(keys_only=True)
            if None is not key:
                return key.get()

    @classmethod
    def is_unique(cls, name):
        distributor = cls.find_by_name(name)
        if distributor is not None and name == name:
            return False
        else:
            return True

    @classmethod
    def create(cls,
               name,
               active=True,
               content_manager_url=config.DEFAULT_CONTENT_MANAGER_URL,
               player_content_url=config.DEFAULT_PLAYER_CONTENT_URL):
        distributor_entity_group = DistributorEntityGroup.singleton()
        return cls(parent=distributor_entity_group.key,
                   name=name,
                   content_manager_url=content_manager_url,
                   player_content_url=player_content_url,
                   active=active)

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class Domain(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    distributor_key = ndb.KeyProperty(kind=Distributor, required=True, indexed=True)
    impersonation_admin_email_address = ndb.StringProperty(required=True, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Domain.query(Domain.name == name).get(keys_only=True)
            if None is not key:
                return key.get()

    @classmethod
    def create(cls, name, distributor_key, impersonation_admin_email_address, active):
        return cls(distributor_key=distributor_key,
                   name=name,
                   impersonation_admin_email_address=impersonation_admin_email_address,
                   active=active)

    def _pre_put_hook(self):
        self.class_version = 1


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
    class_version = ndb.IntegerProperty()

    def get_domain(self):
        return self.domain_key.get()

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Tenant.query(Tenant.name == name).get(keys_only=True)
            if None is not key:
                return key.get()

    @classmethod
    def find_by_tenant_code(cls, tenant_code):
        if tenant_code:
            key = Tenant.query(Tenant.tenant_code == tenant_code).get(keys_only=True)
            if None is not key:
                return key.get()

    @classmethod
    def is_tenant_code_unique(cls, tenant_code):
        return None is Tenant.query(Tenant.tenant_code == tenant_code).get(keys_only=True)

    @classmethod
    def find_devices(cls, tenant_key, unmanaged):
        if tenant_key:
            return ChromeOsDevice.query(
                ndb.AND(ChromeOsDevice.tenant_key == tenant_key,
                        ChromeOsDevice.is_unmanaged_device == unmanaged)
            ).fetch(1000)

    @classmethod
    def get_impersonation_email(cls, urlsafe_tenant_key):
        if urlsafe_tenant_key:
            tenant = ndb.Key(urlsafe=urlsafe_tenant_key).get()
            urlsafe_domain_key = tenant.domain_key.urlsafe()
            domain = ndb.Key(urlsafe=urlsafe_domain_key).get()
            return domain.impersonation_admin_email_address

    @classmethod
    def create(cls, tenant_code, name, admin_email, content_server_url, domain_key, active,
               content_manager_base_url, notification_emails=[], proof_of_play_logging=False):
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
                   proof_of_play_logging=proof_of_play_logging)

    @classmethod
    def toggle_proof_of_play(cls, tenant_code, enable):
        tenant = Tenant.find_by_tenant_code(tenant_code)
        managed_devices = Tenant.find_devices(tenant.key, unmanaged=False)
        for device in managed_devices:
            if not enable:
                device.proof_of_play_logging = enable
            device.proof_of_play_editable = enable
            device.put()
        tenant.proof_of_play_logging = enable
        tenant.put()

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class Location(ndb.Model):
    tenant_key = ndb.KeyProperty(kind=Tenant, required=True, indexed=True)
    customer_location_code = ndb.StringProperty(required=True, indexed=True)
    customer_location_name = ndb.StringProperty(required=True, indexed=True)
    timezone = ndb.StringProperty(required=True, indexed=True)
    timezone_offset = ndb.IntegerProperty(required=True, indexed=True)  # computed property
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
    def create(cls, tenant_key, customer_location_name, customer_location_code, timezone):
        timezone_offset = TimezoneUtil.get_timezone_offset(timezone)
        geo_location_default = ndb.GeoPt(44.98, -93.27)  # Home plate Target Field
        return cls(tenant_key=tenant_key,
                   customer_location_name=customer_location_name,
                   customer_location_code=customer_location_code,
                   timezone=timezone,
                   geo_location=geo_location_default,
                   timezone_offset=timezone_offset)

    @classmethod
    def find_by_customer_location_code(cls, customer_location_code):
        if customer_location_code:
            key = Location.query(Location.customer_location_code == customer_location_code).get(keys_only=True)
            if None is not key:
                return key.get()

    @classmethod
    def is_customer_location_code_unique(cls, customer_location_code, tenant_key):
        return None is Location.query(
            ndb.AND(Location.customer_location_code == customer_location_code, Location.tenant_key == tenant_key)).get(
            keys_only=True)

    def _pre_put_hook(self):
        self.class_version = 1


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
    proof_of_play_logging = ndb.BooleanProperty(default=False, required=True, indexed=True)
    proof_of_play_editable = ndb.BooleanProperty(default=False, required=True)
    customer_display_name = ndb.StringProperty(required=False, indexed=True)
    customer_display_code = ndb.StringProperty(required=False, indexed=True)
    location_key = ndb.KeyProperty(required=False, indexed=True)
    class_version = ndb.IntegerProperty()

    def get_tenant(self):
        return self.tenant_key.get()

    @classmethod
    def get_by_device_id(cls, device_id):
        if device_id:
            chrome_os_device_key = ChromeOsDevice.query(ChromeOsDevice.device_id == device_id).get(keys_only=True)
            if None is not chrome_os_device_key:
                return chrome_os_device_key.get()

    @classmethod
    def create_managed(cls, tenant_key, gcm_registration_id, mac_address, device_id=None, serial_number=None,
                       model=None):
        device = cls(
            device_id=device_id,
            tenant_key=tenant_key,
            gcm_registration_id=gcm_registration_id,
            mac_address=mac_address,
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
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES)
        return device

    @classmethod
    def create_unmanaged(cls, gcm_registration_id, mac_address):
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
            heartbeat_interval_minutes=config.PLAYER_HEARTBEAT_INTERVAL_MINUTES)
        return device

    @classmethod
    def get_unmanaged_device_by_mac_address(cls, mac_address):
        if mac_address:
            device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.mac_address == mac_address,
                                                      ChromeOsDevice.is_unmanaged_device == True)).get(keys_only=True)
            if None is device_key:
                return None
            else:
                return device_key.get()
        else:
            return None

    @classmethod
    def get_unmanaged_device_by_gcm_registration_id(cls, gcm_registration_id):
        if gcm_registration_id:
            device_key = ChromeOsDevice.query(ndb.AND(ChromeOsDevice.gcm_registration_id == gcm_registration_id,
                                                      ChromeOsDevice.is_unmanaged_device == True)).get(keys_only=True)
            if None is device_key:
                return None
            else:
                return device_key.get()
        else:
            return None

    @classmethod
    def mac_address_already_assigned(cls, device_mac_address):
        mac_address_assigned_to_device = ChromeOsDevice.query(
            ndb.OR(ChromeOsDevice.mac_address == device_mac_address,
                   ChromeOsDevice.ethernet_mac_address == device_mac_address)).count() > 0
        return mac_address_assigned_to_device

    @classmethod
    def is_rogue_unmanaged_device(cls, mac_address):
        device = ChromeOsDevice.get_unmanaged_device_by_mac_address(mac_address)
        if device is not None and device.pairing_code is not None and device.tenant_key is None:
            return True
        else:
            return False

    def _pre_put_hook(self):
        self.class_version = 3


@ae_ndb_serializer
class DeviceIssueLog(ndb.Model):
    device_key = ndb.KeyProperty(kind=ChromeOsDevice, required=True, indexed=True)
    category = ndb.StringProperty(required=True, indexed=True)
    up = ndb.BooleanProperty(default=True, required=False, indexed=True)
    program = ndb.StringProperty(required=False, indexed=True)
    program_id = ndb.StringProperty(required=False, indexed=True)
    last_error = ndb.StringProperty(required=False, indexed=True)
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
    def create(cls, device_key, category, up=True, storage_utilization=0, memory_utilization=0,
               program=None, program_id=None, last_error=None, resolved=False, resolved_datetime=None):
        if category in [config.DEVICE_ISSUE_MEMORY_HIGH, config.DEVICE_ISSUE_STORAGE_LOW]:
            level = IssueLevel.Warning
            level_descriptor = IssueLevel.stringify(IssueLevel.Warning)
        elif category in [config.DEVICE_ISSUE_PLAYER_DOWN]:
            level = IssueLevel.Danger
            level_descriptor = IssueLevel.stringify(IssueLevel.Danger)
        else:
            level = IssueLevel.Normal
            level_descriptor = IssueLevel.stringify(IssueLevel.Normal)
        return cls(device_key=device_key,
                   category=category,
                   up=up,
                   storage_utilization=storage_utilization,
                   memory_utilization=memory_utilization,
                   program=program,
                   program_id=program_id,
                   last_error=last_error,
                   resolved=resolved,
                   resolved_datetime=resolved_datetime,
                   level=level,
                   level_descriptor=level_descriptor)

    @classmethod
    def no_matching_issues(cls, device_key, category, up=True, storage_utilization=0, memory_utilization=0,
                           program=None, program_id=None, last_error=None):
        issues = DeviceIssueLog.query(DeviceIssueLog.device_key == device_key,
                                      ndb.AND(DeviceIssueLog.category == category),
                                      ndb.AND(DeviceIssueLog.storage_utilization == storage_utilization),
                                      ndb.AND(DeviceIssueLog.memory_utilization == memory_utilization),
                                      ndb.AND(DeviceIssueLog.up == up),
                                      ndb.AND(DeviceIssueLog.resolved == False)
                                      ).get(keys_only=True)
        return None == issues

    @classmethod
    def device_not_reported(cls, device_key):
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
                issue.level = IssueLevel.Warning
                issue.level_descriptor = IssueLevel.stringify(IssueLevel.Warning)
            elif category in [config.DEVICE_ISSUE_PLAYER_DOWN]:
                issue.level = IssueLevel.Danger
                issue.level_descriptor = IssueLevel.stringify(IssueLevel.Danger)
            else:
                issue.level = IssueLevel.Normal
                issue.level_descriptor = IssueLevel.stringify(IssueLevel.Normal)
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
                issue.level = IssueLevel.Warning
                issue.level_descriptor = IssueLevel.stringify(IssueLevel.Warning)
            elif category in [config.DEVICE_ISSUE_PLAYER_DOWN]:
                issue.level = IssueLevel.Danger
                issue.level_descriptor = IssueLevel.stringify(IssueLevel.Danger)
            else:
                issue.level = IssueLevel.Normal
                issue.level_descriptor = IssueLevel.stringify(IssueLevel.Normal)
            issue.resolved_datetime = resolved_datetime
            issue.put()

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class User(ndb.Model):
    class_version = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty(required=True)
    is_administrator = ndb.BooleanProperty(default=False)
    stormpath_account_href = ndb.StringProperty()
    last_login = ndb.DateTimeProperty()
    enabled = ndb.BooleanProperty(default=True)

    def _pre_put_hook(self):
        self.class_version = 1
        if self.key is None or self.key.id() is None:
            self.key = ndb.Key(User, self.email.lower())

    @classmethod
    def _build_key(cls, email):
        key = ndb.Key(User, email.lower())
        return key

    @classmethod
    def get_or_insert_by_email(cls, email, stormpath_account_href=None):
        user = cls.get_by_email(email)
        if user is None:
            key = cls._build_key(email)
            user = User(key=key, email=email, stormpath_account_href=stormpath_account_href)
            user.put()
        else:
            if user.stormpath_account_href != stormpath_account_href and stormpath_account_href is not None:
                user.stormpath_account_href = stormpath_account_href
                user.put()
        return user

    @classmethod
    def get_by_email(cls, email):
        key = cls._build_key(email)
        return key.get()

    @classmethod
    def update_or_create_with_api_account(cls, account):
        user = None
        if account and account.href:
            user = cls.query(cls.stormpath_account_href == account.href).get()
            if user is None:
                user = cls.get_or_insert_by_email(account.email, stormpath_account_href=account.href)
        return user

    @classmethod
    def test_create(cls, email, stormpath_account_href='https://api.stormpath.com/v1/accounts/'):
        return cls(email=email,
                   stormpath_account_href=stormpath_account_href)

    @property
    def distributor_keys(self):
        dist_user_keys = DistributorUser.query(DistributorUser.user_key == self.key).fetch(keys_only=True)
        dist_users = ndb.get_multi(dist_user_keys)
        return [du.distributor_key for du in dist_users]

    @property
    def distributors(self):
        return ndb.get_multi(self.distributor_keys)

    def add_distributor(self, distributor_key):
        if distributor_key not in self.distributor_keys:
            dist_user = DistributorUser(user_key=self.key, distributor_key=distributor_key)
            dist_user.put()


@ae_ndb_serializer
class DistributorUser(ndb.Model):
    """
    Many-to-many relationship between Distributor and User.  Similar to Tenant-User relationship ("Permit") in SKD
    Is there a better name for this?
    """
    class_version = ndb.IntegerProperty()
    distributor_key = ndb.KeyProperty(kind=Distributor, required=True)
    user_key = ndb.KeyProperty(kind=User, required=True)

    @classmethod
    def create(cls, distributor_key, user_key):
        distributor_user = cls(
            user_key=user_key,
            distributor_key=distributor_key)
        return distributor_user

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class PlayerCommandEvent(ndb.Model):
    device_urlsafe_key = ndb.StringProperty(required=True, indexed=True)
    payload = ndb.StringProperty(required=True, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=True, indexed=True)
    gcm_message_id = ndb.StringProperty(required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    posted = ndb.DateTimeProperty(required=True, indexed=True)
    confirmed = ndb.DateTimeProperty(required=False, indexed=True)
    player_has_confirmed = ndb.BooleanProperty(default=False, required=True, indexed=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def create(cls, device_urlsafe_key, payload, gcm_registration_id, player_has_confirmed=False):
        return cls(device_urlsafe_key=device_urlsafe_key,
                   payload=payload,
                   gcm_registration_id=gcm_registration_id,
                   player_has_confirmed=player_has_confirmed,
                   posted=datetime.utcnow())

    @classmethod
    def get_events_by_device_key(self, device_urlsafe_key, last_number=100):
        query = PlayerCommandEvent.query(PlayerCommandEvent.device_urlsafe_key == device_urlsafe_key).order(
            -PlayerCommandEvent.posted)
        return query.fetch(last_number)

    def _pre_put_hook(self):
        self.class_version = 1


class IssueLevel:
    Normal, Warning, Danger = range(3)

    @classmethod
    def stringify(cls, enumeration):
        if enumeration == cls.Normal:
            return 'normal'
        elif enumeration == cls.Warning:
            return 'warning'
        elif enumeration == cls.Danger:
            return 'danger'
        else:
            return None
