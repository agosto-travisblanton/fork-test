import logging
from google.appengine.ext import ndb
from migration_base import MigrationBase
from models import Tenant, TenantEntityGroup, ChromeOsDevice
from chrome_os_devices_api import (refresh_chrome_os_device)

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class RefreshChromeDevicePropertiesFromDirectoryApi(MigrationBase):
    MIGRATION_NAME = 'refresh_chrome_device_properties_from_directory_api'

    def __init__(self):
        super(RefreshChromeDevicePropertiesFromDirectoryApi, self).__init__(self.MIGRATION_NAME)

    def run(self):
        logging.info('Migration {0}: Running'.format(self.MIGRATION_NAME))
        tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        active_tenants = filter(lambda x: x.active is True, tenants)
        for tenant in active_tenants:
            tenant_key = ndb.Key(urlsafe=tenant.key.urlsafe())
            devices = ChromeOsDevice.query(ChromeOsDevice.tenant_key == tenant_key).fetch()
            for device in devices:
                refresh_chrome_os_device(device_urlsafe_key=device.key.urlsafe())
