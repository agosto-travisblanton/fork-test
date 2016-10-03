from migration_base import MigrationBase
from models import Tenant


class SetTenantOverlaysAvailableToFalse(MigrationBase):
    MIGRATION_NAME = 'set_tenant_overlays_available_to_false'

    def __init__(self):
        super(SetTenantOverlaysAvailableToFalse, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_tenant_entities = Tenant.query().fetch()

        for each_entity in all_tenant_entities:
            if not each_entity.overlays_available:
                each_entity.overlays_available = False
                each_entity.put()
