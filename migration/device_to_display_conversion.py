from migration_base import MigrationBase
import logging
import time
from models import AppliedMigration

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DeviceToDisplayConversion(MigrationBase):
    MIGRATION_NAME = '0001_device_to_display_conversion'

    def __init__(self):
        super(DeviceToDisplayConversion, self).__init__(self.MIGRATION_NAME)

    def run(self):
        if AppliedMigration.has_not_been_run(self.MIGRATION_NAME):
            logging.info('Running {0}'.format(self.MIGRATION_NAME))
            time.sleep(5)
            logging.info('Finished {0}'.format(self.MIGRATION_NAME))
