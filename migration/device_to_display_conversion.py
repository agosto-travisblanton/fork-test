import logging
from migration_base import MigrationBase

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DeviceToDisplayConversion(MigrationBase):
    MIGRATION_NAME = 'device_to_display_conversion'

    def __init__(self):
        super(DeviceToDisplayConversion, self).__init__(self.MIGRATION_NAME)

    def run(self):
        logging.info('Running {0}'.format(self.MIGRATION_NAME))

            # device_id = ndb.StringProperty(required=True, indexed=True)
            # gcm_registration_id = ndb.StringProperty(required=True)
            # mac_address = ndb.StringProperty(required=True, indexed=True)
            # api_key = ndb.StringProperty(required=True, indexed=True)
            # serial_number = ndb.StringProperty(required=False, indexed=True)
            # model = ndb.StringProperty(required=False, indexed=True)
            # name = ndb.ComputedProperty(lambda self: '{0} {1}'.format(self.serial_number, self.model))
            # class_version = ndb.IntegerProperty()

            # tenant_key = ndb.KeyProperty(required=True, indexed=True)
            # created = ndb.DateTimeProperty(auto_now_add=True)
            # updated = ndb.DateTimeProperty(auto_now=True)
            # device_id = ndb.StringProperty(required=False, indexed=True)
            # gcm_registration_id = ndb.StringProperty(required=True)
            # mac_address = ndb.StringProperty(required=True, indexed=True)
            # api_key = ndb.StringProperty(required=True, indexed=True)
            # serial_number = ndb.StringProperty(required=False, indexed=True)
            # managed_display = ndb.BooleanProperty(default=True, required=True, indexed=True)
            # status = ndb.StringProperty(required=False, indexed=False)
            # last_sync = ndb.StringProperty(required=False, indexed=False)
            # kind = ndb.StringProperty(required=False, indexed=False)
            # ethernet_mac_address = ndb.StringProperty(required=False, indexed=True)
            # org_unit_path = ndb.StringProperty(required=False, indexed=False)
            # annotated_user = ndb.StringProperty(required=False, indexed=False)
            # annotated_location = ndb.StringProperty(required=False, indexed=False)
            # notes = ndb.StringProperty(required=False, indexed=False)
            # boot_mode = ndb.StringProperty(required=False, indexed=False)
            # last_enrollment_time = ndb.StringProperty(required=False, indexed=False)
            # platform_version = ndb.StringProperty(required=False, indexed=False)
            # model = ndb.StringProperty(required=False, indexed=False)
            # os_version = ndb.StringProperty(required=False, indexed=False)
            # firmware_version = ndb.StringProperty(required=False, indexed=False)
            # class_version = ndb.IntegerProperty()


