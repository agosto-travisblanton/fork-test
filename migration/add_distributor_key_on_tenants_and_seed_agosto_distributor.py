import logging

from google.appengine.ext import ndb

from migration_base import MigrationBase
from models import Tenant, Distributor

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class AddDistributorKeyOnTenantsAndSeedAgostoDistributor(MigrationBase):
    MIGRATION_NAME = 'add_distributor_key_on_tenants_and_seed_agosto_distributor'
    AGOSTO_DISTRIBUTOR_NAME = 'Agosto'

    def __init__(self):
        super(AddDistributorKeyOnTenantsAndSeedAgostoDistributor, self).__init__(self.MIGRATION_NAME)

    def run(self):
        agosto_distributor = Distributor.find_by_name(self.AGOSTO_DISTRIBUTOR_NAME)
        if agosto_distributor is None:
            agosto_distributor = Distributor.create(name=self.AGOSTO_DISTRIBUTOR_NAME, active=True)
        distributor_key = ndb.Key(urlsafe=agosto_distributor.key.urlsafe())
        tenants = Tenant.query()
        for tenant in tenants:
            tenant.distributor_key = distributor_key
            tenant.put()
            tally = '<<{0}>> tenant.name={1} assigned distributor of {2}.'.format(
                self.MIGRATION_NAME, tenant.name, agosto_distributor.name)
            logging.debug(tally)
