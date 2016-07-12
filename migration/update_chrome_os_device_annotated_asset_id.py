import logging

from google.appengine.ext import ndb
from google.appengine.ext.deferred import deferred

from migration_base import MigrationBase
from models import Tenant, TenantEntityGroup
from workflow.update_chrome_os_device import update_chrome_os_device

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>, Chris Bartling <chris.bartling@agosto.com>'


class UpdateChromeOsDeviceAnnotatedAssetId(MigrationBase):
    MIGRATION_NAME = 'update_chrome_os_device_annotated_asset_id'

    def __init__(self):
        super(UpdateChromeOsDeviceAnnotatedAssetId, self).__init__(self.MIGRATION_NAME)

    def run(self):
        logging.info('Migration {0}: Running'.format(self.MIGRATION_NAME))
        tenants = Tenant.query(ancestor=TenantEntityGroup.singleton().key)
        active_tenants = filter(lambda x: x.active is True, tenants)
        for tenant in active_tenants:
            tenant_key = ndb.Key(urlsafe=tenant.key.urlsafe())
            devices = Tenant.find_devices(tenant_key)
            for device in devices:
                deferred.defer(update_chrome_os_device,
                               device_urlsafe_key=device.key.urlsafe(),
                               _queue='directory-api',
                               _countdown=2)
