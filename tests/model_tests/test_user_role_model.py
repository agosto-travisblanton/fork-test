from tests.provisioning_base_test import ProvisioningBaseTest
from models import UserRole


class TestUserRoleModel(ProvisioningBaseTest):
    def setUp(self):
        super(TestUserRoleModel, self).setUp()

    def test_create_or_get_user_role(self):
        u = UserRole.create_or_get_user_role(1)
        self.assertEqual(u.role, 1)
