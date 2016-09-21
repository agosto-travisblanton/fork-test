from app_config import config
from migration_base import MigrationBase
from model_entities.domain_model import Domain


class SetDefaultOrganizationUnitPathOnDomains(MigrationBase):
    MIGRATION_NAME = 'set_default_organization_unit_path_on_domains'

    def __init__(self):
        super(SetDefaultOrganizationUnitPathOnDomains, self).__init__(self.MIGRATION_NAME)

    def run(self):
        domains = Domain.query().fetch()

        for domain in domains:
            if not domain.organization_unit_path:
                domain.organization_unit_path = config.DEFAULT_OU_PATH
                domain.put()
