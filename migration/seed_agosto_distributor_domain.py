from app_config import config
from migration_base import MigrationBase
from models import Distributor, Domain, DistributorUser, User

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class SeedAgostoDistributorDomain(MigrationBase):
    MIGRATION_NAME = 'seed_agosto_distributor_domain'
    AGOSTO_DISTRIBUTOR_NAME = 'Agosto'
    TIERNEY_DISTRIBUTOR_NAME = 'Tierney Bros., Inc.'

    def __init__(self):
        super(SeedAgostoDistributorDomain, self).__init__(self.MIGRATION_NAME)

    def run(self):
        agosto_distributor = Distributor.find_by_name(self.AGOSTO_DISTRIBUTOR_NAME)
        if agosto_distributor is None:
            agosto_distributor = Distributor.create(name=self.AGOSTO_DISTRIBUTOR_NAME, active=True)
            agosto_distributor.admin_email = 'admin@agosto.com'
            agosto_distributor.put()
        default_domain = config.DEFAULT_AGOSTO_DEVICE_DOMAIN.lower()
        agosto_default_domain = Domain.find_by_name(default_domain)
        if agosto_default_domain is None:
            agosto_default_domain = \
                Domain.create(name=default_domain,
                              distributor_key=agosto_distributor.key,
                              impersonation_admin_email_address=config.IMPERSONATION_ADMIN_EMAIL_ADDRESS,
                              active=True)
            agosto_default_domain.put()
        tierney_distributor = Distributor.find_by_name(self.TIERNEY_DISTRIBUTOR_NAME)
        if tierney_distributor is None:
            tierney_distributor = Distributor.create(name=self.TIERNEY_DISTRIBUTOR_NAME, active=True)
            tierney_distributor.admin_email = 'admin@agosto.com'
            tierney_distributor.put()
