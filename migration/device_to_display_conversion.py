import logging
from google.appengine.ext import ndb
from migration_base import MigrationBase
from models import Tenant, TenantEntityGroup, ChromeOsDevice, Display
from chrome_os_devices_api import (refresh_display)

from google.appengine.ext.deferred import deferred

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DeviceToDisplayConversion(MigrationBase):
    MIGRATION_NAME = 'device_to_display_conversion'

    def __init__(self):
        super(DeviceToDisplayConversion, self).__init__(self.MIGRATION_NAME)

    @staticmethod
    def get_displays_by_tenant(key):
        tenant_key = ndb.Key(urlsafe=key)
        displays = Display.query(Display.tenant_key == tenant_key)
        return displays

    def run(self):
        logging.info('Migration {0}: Running'.format(self.MIGRATION_NAME))
        tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key).fetch(100)
        active_tenants = filter(lambda x: x.active is True, tenants)
        for tenant in active_tenants:
            tenant_key = ndb.Key(urlsafe=tenant.key.urlsafe())
            devices = ChromeOsDevice.query(ancestor=tenant_key).fetch()
            number_of_devices = len(devices)
            number_of_existing_displays = 0
            number_of_new_displays = 0
            for device in devices:
                existing_display = Display.get_by_device_id(device.device_id)
                if existing_display is not None:
                    number_of_existing_displays += 1
                    deferred.defer(refresh_display, display_urlsafe_key=existing_display.key.urlsafe())
                else:
                    display = Display(tenant_key=tenant_key,
                                      gcm_registration_id=device.gcm_registration_id,
                                      mac_address=device.mac_address,
                                      device_id=device.device_id,
                                      api_key=device.api_key)
                    key = display.put()
                    logging.info('Migration {0}: Created display with mac_address={1}'.format(self.MIGRATION_NAME,
                                                                                              device.mac_address))
                    number_of_new_displays += 1
                    deferred.defer(refresh_display, display_urlsafe_key=key.urlsafe())
            final_tally = 'Migration {0}: Devices={1}, New Displays={2}, Existing Displays={3}'.format(
                self.MIGRATION_NAME, number_of_devices, number_of_new_displays, number_of_existing_displays)
            logging.info(final_tally)
