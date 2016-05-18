from env_setup import setup_test_paths

setup_test_paths()
from tests.provisioning_base_test import ProvisioningBaseTest
from models import DistributorUser, User, Distributor


class TestDistributerUserModel(ProvisioningBaseTest):
    def setUp(self):
        super(TestDistributerUserModel, self).setUp()

        self.user = User(email="chris@mycompany.com")
        self.user_key = self.user.put()
        self.agosto = Distributor.create(name='Agosto',
                                         active=True)

        self.agosto_key = self.agosto.put()

    def test_create_distributor_user_associations(self):
        distributor_user1 = DistributorUser.create(user_key=self.user_key, distributor_key=self.agosto_key)
        distributor_user1.put()

        self.assertEqual(distributor_user1.role.get().role, 0)
        self.assertEqual(distributor_user1.user_key, self.user_key)
        self.assertEqual(distributor_user1.distributor_key, self.agosto_key)