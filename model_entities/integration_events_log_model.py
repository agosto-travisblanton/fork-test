import uuid

from datetime import datetime
from google.appengine.ext import ndb

from restler.decorators import ae_ndb_serializer


@ae_ndb_serializer
class IntegrationEventLog(ndb.Model):
    event_category = ndb.StringProperty(required=True, indexed=True)
    correlation_identifier = ndb.StringProperty(required=True, indexed=True)
    component_name = ndb.StringProperty(required=True, indexed=True)
    workflow_step = ndb.StringProperty(required=True, indexed=True)
    utc_timestamp = ndb.DateTimeProperty(required=True, indexed=True)

    device_urlsafe_key = ndb.StringProperty(required=False, indexed=True)
    serial_number = ndb.StringProperty(required=False, indexed=True)
    tenant_code = ndb.StringProperty(required=False, indexed=True)
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
               device_urlsafe_key=None,
               serial_number=None,
               tenant_code=None,
               gcm_registration_id=None,
               mac_address=None,
               details=None,
               utc_timestamp=None):
        if correlation_identifier:
            correlation_id = correlation_identifier
        else:
            correlation_id = cls.generate_correlation_id()
        if utc_timestamp:
            timestamp = utc_timestamp
        else:
            timestamp = datetime.utcnow()
        return cls(event_category=event_category,
                   component_name=component_name,
                   workflow_step=workflow_step,
                   correlation_identifier=correlation_id,
                   device_urlsafe_key=device_urlsafe_key,
                   serial_number=serial_number,
                   tenant_code=tenant_code,
                   gcm_registration_id=gcm_registration_id,
                   mac_address=mac_address,
                   details=details,
                   utc_timestamp=timestamp)

    @classmethod
    def generate_correlation_id(cls):
        return str(uuid.uuid4().hex)

    @classmethod
    def get_correlation_identifier_for_registration(cls, device_urlsafe_key):
        events = IntegrationEventLog.query(
            ndb.AND(IntegrationEventLog.event_category == 'Registration',
                    IntegrationEventLog.device_urlsafe_key == device_urlsafe_key)).fetch()
        if len(events) > 0:
            return events[0].correlation_identifier
        else:
            return None

    def _pre_put_hook(self):
        self.class_version = 1
