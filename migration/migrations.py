import logging
from datetime import time
from migration.migration_base import MigrationBase

__author__ = 'chris'


class SomethingMigration(MigrationBase):
    def __init__(self):
        super(SomethingMigration, self).__init__('It does something!')

    def run(self):
        logging.info('START: Something migration...')
        time.sleep(5)
        logging.info('FINISH: Something migration')
