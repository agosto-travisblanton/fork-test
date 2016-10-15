from migration_base import MigrationBase
from models import ChromeOsDevice


class SetOverlayStatusToFalse(MigrationBase):
    MIGRATION_NAME = 'set_overlay_status_to_false'

    def __init__(self):
        super(SetOverlayStatusToFalse, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_device_entities = ChromeOsDevice.query().fetch()

        for each_entity in all_device_entities:
            if not each_entity.overlays_available:
                each_entity.overlays_available = False
                each_entity.put()
