from migration_base import MigrationBase
from models import ChromeOsDevice


class HydrateDefaultDeviceSleepProperty(MigrationBase):
    MIGRATION_NAME = 'hydrate_default_device_sleep_property'

    def __init__(self):
        super(HydrateDefaultDeviceSleepProperty, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_device_entities = ChromeOsDevice.query().fetch()

        for each_entity in all_device_entities:
            each_entity.panel_sleep = True
            each_entity.put()
