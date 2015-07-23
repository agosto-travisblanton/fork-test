import logging
import uuid

from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'

TENANT_ENTITY_GROUP_NAME = 'tenantEntityGroup'
DISTRIBUTOR_ENTITY_GROUP_NAME = 'distributorEntityGroup'


class TenantEntityGroup(ndb.Model):
    name = ndb.StringProperty(required=True)

    @classmethod
    def singleton(cls):
        return TenantEntityGroup.get_or_insert(TENANT_ENTITY_GROUP_NAME,
                                               name=TENANT_ENTITY_GROUP_NAME)


class DistributorEntityGroup(ndb.Model):
    name = ndb.StringProperty(required=True)

    @classmethod
    def singleton(cls):
        return DistributorEntityGroup.get_or_insert(DISTRIBUTOR_ENTITY_GROUP_NAME,
                                                    name=DISTRIBUTOR_ENTITY_GROUP_NAME)


@ae_ndb_serializer
class Distributor(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)

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


@ae_ndb_serializer
class Tenant(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    tenant_code = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    admin_email = ndb.StringProperty(required=True)
    content_server_url = ndb.StringProperty(required=True)
    chrome_device_domain = ndb.StringProperty()
    active = ndb.BooleanProperty(default=True, required=True, indexed=True)

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Tenant.query(Tenant.name == name).get(keys_only=True)
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
    def create(cls, tenant_code, name, admin_email, content_server_url, chrome_device_domain, active):
        tenant_entity_group = TenantEntityGroup.singleton()
        return cls(parent=tenant_entity_group.key,
                   tenant_code=tenant_code,
                   name=name,
                   admin_email=admin_email,
                   content_server_url=content_server_url,
                   chrome_device_domain=chrome_device_domain,
                   active=active)


@ae_ndb_serializer
class ChromeOsDevice(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    device_id = ndb.StringProperty(required=True, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=True)
    mac_address = ndb.StringProperty(required=True, indexed=True)
    api_key = ndb.StringProperty(required=True, indexed=True)
    serial_number = ndb.StringProperty(required=False, indexed=True)

    @classmethod
    def get_by_device_id(cls, device_id):
        if device_id:
            chrome_os_device_key = ChromeOsDevice.query(ChromeOsDevice.device_id == device_id).get(keys_only=True)
            if None is not chrome_os_device_key:
                return chrome_os_device_key.get()

    @classmethod
    def create(cls, tenant_key, device_id, gcm_registration_id, mac_address, serial_number=None):
        logging.info("ChromeOsDevice.create....")
        logging.info("  Tenant key: {0}".format(str(tenant_key)))
        api_key = str(uuid.uuid4())
        chrome_os_device = cls(parent=tenant_key,
                               device_id=device_id,
                               gcm_registration_id=gcm_registration_id,
                               mac_address=mac_address,
                               api_key=api_key,
                               serial_number=serial_number)
        return chrome_os_device


@ae_ndb_serializer
class Display(ndb.Model):
    tenant_key = ndb.KeyProperty(required=True, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    device_id = ndb.StringProperty(required=False, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=True)
    mac_address = ndb.StringProperty(required=True, indexed=True)
    api_key = ndb.StringProperty(required=True, indexed=True)
    serial_number = ndb.StringProperty(required=False, indexed=True)
    managed_display = ndb.BooleanProperty(default=True, required=True, indexed=True)

    @classmethod
    def get_by_device_id(cls, device_id):
        if device_id:
            display = Display.query(Display.device_id == device_id).get(keys_only=True)
            if None is not display:
                return display.get()

    @classmethod
    def create(cls, tenant_key, gcm_registration_id, mac_address, device_id=None, serial_number=None,
               managed_display=True):
        display = cls(tenant_key=tenant_key,
                      device_id=device_id,
                      gcm_registration_id=gcm_registration_id,
                      mac_address=mac_address,
                      api_key=str(uuid.uuid4()),
                      serial_number=serial_number,
                      managed_display=managed_display)
        return display
