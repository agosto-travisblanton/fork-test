from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


@ae_ndb_serializer
class Tenant(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True, indexed=True)

    @classmethod
    def find_by_name(cls, name):
        if name:
            key = Tenant.query(Tenant.name == name).get(keys_only=True)
            if None is not key:
                return key.get()


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


