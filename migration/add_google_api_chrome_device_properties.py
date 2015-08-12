import logging
from google.appengine.ext import ndb
from migration_base import MigrationBase
from models import Tenant, TenantEntityGroup, ChromeOsDevice, Display
from chrome_os_devices_api import (refresh_display)

from google.appengine.ext.deferred import deferred

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class AddGoogleApiChromeDeviceProperties(MigrationBase):
    MIGRATION_NAME = 'add_google_api_chrome_device_properties'

    def __init__(self):
        super(AddGoogleApiChromeDeviceProperties, self).__init__(self.MIGRATION_NAME)

    def run(self):
        pass
