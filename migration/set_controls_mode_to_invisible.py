from migration_base import MigrationBase
from models import ChromeOsDevice


class SetControlsModeToInvisible(MigrationBase):
    MIGRATION_NAME = 'set_controls_mode_to_invisible'
    default_value = 'invisible'

    def __init__(self):
        super(SetControlsModeToInvisible, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_device_entities = ChromeOsDevice.query().fetch()

        for each_entity in all_device_entities:
            if not each_entity.controls_mode:
                each_entity.controls_mode = self.default_value
                each_entity.put()
