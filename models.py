import uuid

from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer

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
    def create(cls, name, active):
        distributor_entity_group = DistributorEntityGroup.singleton()
        return cls(parent=distributor_entity_group.key,
                   name=name,
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
    def is_unique(cls, name):
        tenant = cls.find_by_name(name)
        if tenant is not None and name == name:
            return False
        else:
            return True

    @classmethod
    def find_devices(cls, tenant_key):
        if tenant_key:
            return ChromeOsDevice.query(ChromeOsDevice.tenant_key == tenant_key).fetch(1000)

    @classmethod
    def get_impersonation_email(cls, urlsafe_tenant_key):
        if urlsafe_tenant_key:
            tenant = ndb.Key(urlsafe=urlsafe_tenant_key).get()
            urlsafe_domain_key = tenant.domain_key.urlsafe()
            domain = ndb.Key(urlsafe=urlsafe_domain_key).get()
            return domain.impersonation_admin_email_address

    @classmethod
    def create(cls, tenant_code, name, admin_email, content_server_url, domain_key, active,
               content_manager_base_url):
        tenant_entity_group = TenantEntityGroup.singleton()
        return cls(parent=tenant_entity_group.key,
                   tenant_code=tenant_code,
                   name=name,
                   admin_email=admin_email,
                   content_server_url=content_server_url,
                   domain_key=domain_key,
                   active=active,
                   content_manager_base_url=content_manager_base_url)

    def _pre_put_hook(self):
        self.class_version = 1


@ae_ndb_serializer
class ChromeOsDevice(ndb.Model):
    tenant_key = ndb.KeyProperty(required=True, indexed=True)
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
    os_version = ndb.StringProperty(required=False, indexed=False)
    firmware_version = ndb.StringProperty(required=False, indexed=False)
    etag = ndb.StringProperty(required=False, indexed=False)
    name = ndb.ComputedProperty(lambda self: '{0} {1}'.format(self.serial_number, self.model))
    loggly_link = ndb.ComputedProperty(lambda self: 'https://skykit.loggly.com/search?&terms=tag%3A"{0}"'.format(
        self.serial_number))
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
    def create(cls, tenant_key, gcm_registration_id, mac_address, device_id=None, serial_number=None, model=None):
        chrome_os_device = cls(
            device_id=device_id,
            tenant_key=tenant_key,
            gcm_registration_id=gcm_registration_id,
            mac_address=mac_address,
            api_key=str(uuid.uuid4().hex),
            serial_number=serial_number,
            model=model)
        return chrome_os_device

    def _pre_put_hook(self):
        self.class_version = 2


@ae_ndb_serializer
class User(ndb.Model):
    class_version = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty(required=True)
    is_administrator = ndb.BooleanProperty(default=False)
    stormpath_account_href = ndb.StringProperty()
    last_login = ndb.DateTimeProperty()

    def _pre_put_hook(self):
        self.class_version = 1
        if self.key is None or self.key.id() is None:
            self.key = ndb.Key(User, self.email)

    @classmethod
    def get_by_email(cls, email):
        return ndb.Key(User, email).get()

    @classmethod
    def update_or_create_with_api_account(cls, account):
        user = None
        if account.href:
            user = cls.query(cls.stormpath_account_href == account.href).get()
            if user is None:
                user = User.get_or_insert(account.email, email=account.email, stormpath_account_href=account.href)
        return user

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
