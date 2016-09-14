from migration_base import MigrationBase
from models import Tenant


class HydrateOrganizationUnitIdToNone(MigrationBase):
    MIGRATION_NAME = 'hydrate_ou_id_to_none'

    def __init__(self):
        super(HydrateOrganizationUnitIdToNone, self).__init__(self.MIGRATION_NAME)

    def run(self):
        all_tenant_entities = Tenant.query().fetch()

        for each_entity in all_tenant_entities:
            if not each_entity.organization_unit_id:
                each_entity.organization_unit_id = None
                each_entity.put()
