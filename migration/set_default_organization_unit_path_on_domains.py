import logging
from app_config import config
from migration_base import MigrationBase
from model_entities.domain_model import Domain

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class SetDefaultOrganizationUnitPathOnDomains(MigrationBase):
    MIGRATION_NAME = 'set_default_organization_unit_path_on_domains'

    def __init__(self):
        super(SetDefaultOrganizationUnitPathOnDomains, self).__init__(self.MIGRATION_NAME)

    def run(self):
        domains = Domain.query().fetch()
        number_of_domains = len(domains)
        tally = '<<{0}>> {1} domains.'.format(self.MIGRATION_NAME, number_of_domains)
        logging.debug(tally)

        for domain in domains:
            if not domain.organization_unit_path:
                domain.organization_unit_path = config.DEFAULT_OU_PATH
                domain.put()
