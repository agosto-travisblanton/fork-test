from env_setup import setup_test_paths
setup_test_paths()

from proofplay.proofplay_models import Base
from proofplay.db import Session, engine
from tests.provisioning_distributor_user_base_test import ProvisioningDistributorUserBase

class SQLBaseTest(ProvisioningDistributorUserBase):
    def setUp(self):
        super(SQLBaseTest, self).setUp()
        Session.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.db_session = Session()

    def tearDown(self):
        Session.remove()
        Base.metadata.drop_all(bind=engine)

