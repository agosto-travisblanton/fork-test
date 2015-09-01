from migration_base import MigrationBase
from models import Distributor

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class SeedAgostoDistributor(MigrationBase):
    MIGRATION_NAME = 'seed_agosto_distributor'
    AGOSTO_DISTRIBUTOR_NAME = 'Agosto'

    def __init__(self):
        super(SeedAgostoDistributor, self).__init__(self.MIGRATION_NAME)

    def run(self):
        agosto_distributor = Distributor.find_by_name(self.AGOSTO_DISTRIBUTOR_NAME.lower())
        if agosto_distributor is None:
            agosto_distributor = Distributor.create(name=self.AGOSTO_DISTRIBUTOR_NAME, active=True)
            agosto_distributor.put()
