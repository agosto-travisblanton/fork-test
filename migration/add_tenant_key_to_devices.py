import logging
from google.appengine.ext import ndb
from migration_base import MigrationBase
from models import Tenant, TenantEntityGroup, ChromeOsDevice, Display
from chrome_os_devices_api import (refresh_display)

from google.appengine.ext.deferred import deferred

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class AddTenantKeyToDevices(MigrationBase):
    MIGRATION_NAME = 'add_tenant_key_to_devices'

    def __init__(self):
        super(AddTenantKeyToDevices, self).__init__(self.MIGRATION_NAME)

    def run(self):
        tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key).fetch(100)
        active_tenants = filter(lambda x: x.active is True, tenants)
        for tenant in active_tenants:
            tenant_key = ndb.Key(urlsafe=tenant.key.urlsafe())
            devices = ChromeOsDevice.query(ancestor=tenant_key).fetch()
            number_of_devices = len(devices)
            number_of_tenant_keys_hydrated = 0
            for device in devices:
                if len(device.tenant_key) < 1:
                    number_of_tenant_keys_hydrated += 1
                    device.tenant_key = tenant_key
                    device.put()
            tally = '{0}: tenant.name={1}, number_of_devices={2}, number_of_tenant_keys_hydrated={3}'.format(
                self.MIGRATION_NAME, tenant.name, number_of_devices, number_of_tenant_keys_hydrated)
            logging.info(tally)
