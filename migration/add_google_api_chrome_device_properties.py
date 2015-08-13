import logging
from google.appengine.ext import ndb
from migration_base import MigrationBase
from models import Tenant, TenantEntityGroup, ChromeOsDevice
from chrome_os_devices_api import (refresh_chrome_os_display)

from google.appengine.ext.deferred import deferred

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class AddGoogleApiChromeDeviceProperties(MigrationBase):
    MIGRATION_NAME = 'add_google_api_chrome_device_properties'

    def __init__(self):
        super(AddGoogleApiChromeDeviceProperties, self).__init__(self.MIGRATION_NAME)

    def run(self):
        logging.debug('Migration {0}: Running'.format(self.MIGRATION_NAME))
        tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key).fetch()
        active_tenants = filter(lambda x: x.active is True, tenants)
        for tenant in active_tenants:
            tenant_key = ndb.Key(urlsafe=tenant.key.urlsafe())
            devices = ChromeOsDevice.query(ChromeOsDevice.tenant_key == tenant_key).fetch()
            number_of_devices = len(devices)
            number_of_refreshed_displays = 0
            for device in devices:
                refresh_chrome_os_display(device_urlsafe_key=device.key.urlsafe())
                number_of_refreshed_displays += 1
            tally = '<<{0}>> tenant.name={1}, number_of_devices={2}, number_of_refreshed_displays={3}'.format(
                self.MIGRATION_NAME, tenant.name, number_of_devices, number_of_refreshed_displays)
            logging.debug(tally)
