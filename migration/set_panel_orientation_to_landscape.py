from migration_base import MigrationBase
from models import ChromeOsDevice


class SetPanelOrientationToLandscape(MigrationBase):
    MIGRATION_NAME = 'set_panel_orientation_to_landscape'

    def __init__(self):
        super(SetPanelOrientationToLandscape, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_device_entities = ChromeOsDevice.query().fetch()

        for each_entity in all_device_entities:
            if not each_entity.orientation_mode:
                each_entity.orientation_mode = 'landscape'
                each_entity.put()
