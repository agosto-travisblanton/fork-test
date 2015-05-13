from google.appengine.ext import ndb
import uuid

from restler.decorators import ae_ndb_serializer

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'

class TenantEntityGroup(ndb.Model):
    name = ndb.StringProperty(required=True)

    @classmethod
    def singleton(cls):
        return TenantEntityGroup.get_or_insert('tenantEntityGroup',
                                               name='tenantEntityGroup')


@ae_ndb_serializer
class Tenant(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True, indexed=True)
    admin_email = ndb.StringProperty(required=True)
    content_server_url = ndb.StringProperty(required=True)
    content_server_api_key = ndb.StringProperty(required=True)
    chrome_device_domain = ndb.StringProperty()
    # make a random UUID for the content_server_api_key to send back to player
    # import uuid
    # uuid.uuid4()
    # UUID('16fd2706-8baf-433b-82eb-8c7fada847da')

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Tenant.query(Tenant.name == name).get(keys_only=True)
            if None is not key:
                return key.get()

    @classmethod
    def create(cls, name, admin_email, content_server_url, chrome_device_domain):
        return cls(name=name,
                   admin_email=admin_email,
                   content_server_url=content_server_url,
                   content_server_api_key=uuid.uuid4(),
                   chrome_device_domain=chrome_device_domain)

@ae_ndb_serializer
class ChromeOsDevice(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    device_id = ndb.StringProperty(required=True, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=True)

    @classmethod
    def get_by_device_id(cls, device_id):
        if device_id:
            chrome_os_device_key = ChromeOsDevice.query(ChromeOsDevice.device_id == device_id).get(keys_only=True)
            if None is not chrome_os_device_key:
                return chrome_os_device_key.get()


