from migration_base import MigrationBase
from models import ChromeOsDevice


class SetAllOrientationToZero(MigrationBase):
    MIGRATION_NAME = 'set_all_orientation_to_zero'

    def __init__(self):
        super(SetAllOrientationToZero, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_device_entities = ChromeOsDevice.query().fetch()

        for each_entity in all_device_entities:
            each_entity.orientation_mode = '0'
            each_entity.put()
