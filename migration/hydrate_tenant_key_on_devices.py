import logging
from google.appengine.ext import ndb
from migration_base import MigrationBase
from models import Tenant, TenantEntityGroup, ChromeOsDevice

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class HydrateTenantKeyOnDevices(MigrationBase):
    MIGRATION_NAME = 'hydrate_tenant_key_on_devices'

    def __init__(self):
        super(HydrateTenantKeyOnDevices, self).__init__(self.MIGRATION_NAME)

    def run(self):
        tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        for tenant in tenants:
            tenant_key = ndb.Key(urlsafe=tenant.key.urlsafe())
            devices = ChromeOsDevice.query(ancestor=tenant_key).fetch()
            number_of_devices = len(devices)
            number_of_tenant_keys_hydrated = 0
            for device in devices:
                if device.tenant_key is None:
                    number_of_tenant_keys_hydrated += 1
                    device.tenant_key = tenant_key
                    device.put()
            tally = '<<{0}>> tenant.name={1}, number_of_devices={2}, number_of_tenant_keys_hydrated={3}'.format(
                self.MIGRATION_NAME, tenant.name, number_of_devices, number_of_tenant_keys_hydrated)
            logging.debug(tally)
