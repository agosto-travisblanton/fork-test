import uuid

from datetime import datetime
from google.appengine.ext import ndb

from chrome_os_device_model import ChromeOsDevice
from location_and_tenant_model import Tenant
from restler.decorators import ae_ndb_serializer


@ae_ndb_serializer
class IntegrationEventLog(ndb.Model):
    event_category = ndb.StringProperty(required=True, indexed=True)
    correlation_identifier = ndb.StringProperty(required=True, indexed=True)
    component_name = ndb.StringProperty(required=True, indexed=True)
    workflow_step = ndb.StringProperty(required=True, indexed=True)
    utc_timestamp = ndb.DateTimeProperty(required=True, indexed=True)

    device_key = ndb.KeyProperty(kind=ChromeOsDevice, required=False, indexed=True)
    tenant_key = ndb.KeyProperty(kind=Tenant, required=False, indexed=True)
    gcm_registration_id = ndb.StringProperty(required=False, indexed=True)
    mac_address = ndb.StringProperty(required=False, indexed=True)
    details = ndb.StringProperty(required=False, indexed=True)

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    class_version = ndb.IntegerProperty()

    @classmethod
    def create(cls,
               event_category,
               component_name,
               workflow_step,
               correlation_identifier=None,
               device_key=None,
               tenant_key=None,
               gcm_registration_id=None,
               mac_address=None,
               details=None,
               utc_timestamp=None):
        if correlation_identifier:
            correlation_id = correlation_identifier
        else:
            correlation_id = str(uuid.uuid4().hex)
        if utc_timestamp:
            timestamp = utc_timestamp
        else:
            timestamp = datetime.utcnow()
        return cls(event_category=event_category,
                   component_name=component_name,
                   workflow_step=workflow_step,
                   correlation_identifier=correlation_id,
                   device_key=device_key,
                   tenant_key=tenant_key,
                   gcm_registration_id=gcm_registration_id,
                   mac_address=mac_address,
                   details=details,
                   utc_timestamp=timestamp)

    def _pre_put_hook(self):
        self.class_version = 1
