import logging
from migration_base import MigrationBase

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class Migration_2(MigrationBase):
    MIGRATION_NAME = 'migration_2'

    def __init__(self):
        super(Migration_2, self).__init__(self.MIGRATION_NAME)

    def run(self):
        logging.info('Running {0}'.format(self.MIGRATION_NAME))
