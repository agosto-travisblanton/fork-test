import logging
from migration_base import MigrationBase

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class DeviceToDisplayConversion(MigrationBase):
    MIGRATION_NAME = 'device_to_display_conversion'

    def __init__(self):
        super(DeviceToDisplayConversion, self).__init__(self.MIGRATION_NAME)

    def run(self):
        logging.info('Running {0}'.format(self.MIGRATION_NAME))
        raise ValueError('A very specific bad thing happened')
