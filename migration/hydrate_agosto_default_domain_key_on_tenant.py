from app_config import config
from migration_base import MigrationBase
from models import Domain, Tenant

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class HydrateAgostoDefaultDomainKeyOnTenant(MigrationBase):
    MIGRATION_NAME = 'hydrate_agosto_default_domain_key_on_tenant'
    AGOSTO_DISTRIBUTOR_NAME = 'Agosto'

    def __init__(self):
        super(HydrateAgostoDefaultDomainKeyOnTenant, self).__init__(self.MIGRATION_NAME)

    def run(self):
        agosto_default_domain = Domain.find_by_name(config.DEFAULT_AGOSTO_DEVICE_DOMAIN)
        tenants = Tenant.query().fetch(1000)
        for tenant in tenants:
            if tenant.domain_key is None:
                tenant.domain_key = agosto_default_domain.key
                tenant.put()
